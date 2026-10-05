// UI de inscripción. Solo usa las operaciones de docs/contrato-api.md.
// Nada de innerHTML: todo texto de usuario/servidor entra con textContent.
(function () {
  "use strict";

  var L = window.Logica;
  var $ = function (id) { return document.getElementById(id); };
  var NIL_UUID = "00000000-0000-0000-0000-000000000000";

  var db = null;
  var modo = "login"; // "login" | "registro"
  var toastTimer = null;

  function el(tag, clase, texto) {
    var n = document.createElement(tag);
    if (clase) n.className = clase;
    if (texto != null) n.textContent = texto;
    return n;
  }

  function mostrarVista(nombre) {
    ["vista-config", "vista-auth", "vista-app"].forEach(function (id) {
      $(id).hidden = id !== nombre;
    });
    $("btn-salir").hidden = nombre !== "vista-app";
  }

  function toast(texto) {
    var t = $("toast");
    t.textContent = texto;
    t.classList.add("visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.classList.remove("visible"); }, 3500);
  }

  function mostrarError(id, texto) {
    var n = $(id);
    n.textContent = texto || "";
    n.hidden = !texto;
  }

  // ---------- Acceso ----------
  function fijarModo(nuevo) {
    modo = nuevo;
    var login = nuevo === "login";
    $("tab-login").setAttribute("aria-selected", String(login));
    $("tab-registro").setAttribute("aria-selected", String(!login));
    $("enviar-auth").textContent = login ? "Iniciar sesión" : "Crear cuenta";
    $("password").setAttribute("autocomplete", login ? "current-password" : "new-password");
    mostrarError("error-auth", "");
  }

  async function enviarAuth(ev) {
    ev.preventDefault();
    var email = $("email").value.trim();
    var password = $("password").value;
    if (!email || !password) {
      mostrarError("error-auth", "Completa el correo y la contraseña.");
      return;
    }
    if (password.length < 6) {
      mostrarError("error-auth", "La contraseña debe tener al menos 6 caracteres.");
      return;
    }
    var boton = $("enviar-auth");
    boton.disabled = true;
    mostrarError("error-auth", "");
    try {
      var res = modo === "login"
        ? await db.auth.signInWithPassword({ email: email, password: password })
        : await db.auth.signUp({ email: email, password: password });
      if (res.error) {
        mostrarError("error-auth", L.traducirError(res.error, modo));
        return;
      }
      if (!res.data || !res.data.session) {
        // Registro con confirmación de correo activa: aún no hay sesión.
        mostrarError("error-auth", "");
        toast("Revisa tu correo para confirmar la cuenta y luego inicia sesión.");
        fijarModo("login");
        return;
      }
      $("password").value = "";
      await entrarApp(res.data.user && res.data.user.email);
    } catch (e) {
      mostrarError("error-auth", L.traducirError(e, modo));
    } finally {
      boton.disabled = false;
    }
  }

  async function salir() {
    var res = await db.auth.signOut();
    if (res && res.error) {
      toast(L.traducirError(res.error, "logout"));
      return;
    }
    mostrarVista("vista-auth");
  }

  // ---------- Talleres e inscripciones ----------
  async function entrarApp(email) {
    $("saludo").textContent = email ? "Sesión iniciada como " + email + "." : "Sesión iniciada.";
    mostrarVista("vista-app");
    await cargarApp();
  }

  async function cargarApp() {
    var estado = $("estado-lista");
    estado.hidden = false;
    estado.textContent = "Cargando talleres…";
    try {
      var r = await Promise.all([
        db.from("talleres").select("id,titulo,descripcion,inicia_en,cupo").order("inicia_en"),
        db.from("inscripciones").select("id,taller_id,nombre,creado_en")
      ]);
      var talleres = r[0], mias = r[1];
      if (talleres.error || mias.error) {
        var err = talleres.error || mias.error;
        if (err.code === "42501" || err.status === 401) { mostrarVista("vista-auth"); return; }
        estado.textContent = L.traducirError(err, "listar");
        return;
      }
      var cupos = await Promise.all((talleres.data || []).map(function (t) {
        return db.rpc("cupos_disponibles", { p_taller_id: t.id }).then(function (x) {
          return x.error ? null : x.data;
        });
      }));
      pintar(talleres.data || [], cupos, mias.data || []);
    } catch (e) {
      estado.textContent = L.traducirError(e, "listar");
    }
  }

  function pintar(talleres, cupos, mias) {
    var porTaller = {};
    mias.forEach(function (i) { porTaller[i.taller_id] = i; });

    var estado = $("estado-lista");
    estado.hidden = talleres.length > 0;
    if (!talleres.length) estado.textContent = "Todavía no hay talleres publicados.";

    var lista = $("lista-talleres");
    lista.replaceChildren();
    talleres.forEach(function (t, idx) {
      var mia = porTaller[t.id];
      var est = L.estadoTaller(cupos[idx], !!mia);
      var li = el("li", "boleto");
      var cuerpo = el("div", "boleto-cuerpo");
      cuerpo.appendChild(el("h3", "boleto-titulo", t.titulo));
      cuerpo.appendChild(el("p", "boleto-fecha", L.formatearFecha(t.inicia_en)));
      if (t.descripcion) cuerpo.appendChild(el("p", "boleto-desc", t.descripcion));
      var talon = el("div", "boleto-talon");
      var textoCupos = el("p", "cupos" + (est === "lleno" ? " lleno" : ""), L.textoCupos(cupos[idx]));
      talon.appendChild(textoCupos);
      if (est === "inscrito") {
        talon.appendChild(el("p", "talon-estado", "Ya estás inscrito"));
      } else {
        var b = el("button", "boton", est === "lleno" ? "Sin cupos" : "Inscribirme");
        b.type = "button";
        b.disabled = est === "lleno";
        b.addEventListener("click", function () { inscribir(t.id, b); });
        talon.appendChild(b);
      }
      li.appendChild(cuerpo);
      li.appendChild(talon);
      lista.appendChild(li);
    });

    var titulos = {};
    talleres.forEach(function (t) { titulos[t.id] = t.titulo; });
    var bloque = $("bloque-mis");
    var listaMis = $("lista-mis");
    listaMis.replaceChildren();
    bloque.hidden = mias.length === 0;
    mias.forEach(function (i) {
      var li = el("li", "boleto entra");
      var cuerpo = el("div", "boleto-cuerpo");
      cuerpo.appendChild(el("h3", "boleto-titulo", titulos[i.taller_id] || "Taller"));
      var talon = el("div", "boleto-talon");
      talon.appendChild(el("p", "talon-estado", "Inscrito"));
      talon.appendChild(el("p", "talon-nombre", i.nombre));
      var b = el("button", "boton secundario", "Cancelar inscripción");
      b.type = "button";
      b.addEventListener("click", function () { cancelar(i.id, b); });
      talon.appendChild(b);
      li.appendChild(cuerpo);
      li.appendChild(talon);
      listaMis.appendChild(li);
    });
  }

  async function inscribir(tallerId, boton) {
    var v = L.validarNombre($("nombre").value);
    if (!v.ok) {
      mostrarError("error-nombre", v.mensaje);
      $("nombre").focus();
      return;
    }
    mostrarError("error-nombre", "");
    boton.disabled = true;
    try {
      var res = await db.from("inscripciones").insert({ taller_id: tallerId, nombre: v.valor }).select();
      if (res.error) {
        toast(L.traducirError(res.error, "inscribir"));
        if (res.error.code === "42501") { mostrarVista("vista-auth"); return; }
      } else {
        toast("Inscripción confirmada.");
      }
      await cargarApp(); // refresca cupos y estado real
    } catch (e) {
      toast(L.traducirError(e, "inscribir"));
      boton.disabled = false;
    }
  }

  async function cancelar(inscripcionId, boton) {
    if (!window.confirm("¿Cancelar tu inscripción? Liberarás tu cupo.")) return;
    boton.disabled = true;
    try {
      var res = await db.from("inscripciones").delete().eq("id", inscripcionId).select();
      if (res.error) toast(L.traducirError(res.error, "cancelar"));
      else if (!res.data || !res.data.length) toast("No encontramos esa inscripción. Actualizamos la lista.");
      else toast("Inscripción cancelada.");
      await cargarApp();
    } catch (e) {
      toast(L.traducirError(e, "cancelar"));
      boton.disabled = false;
    }
  }

  // ---------- Arranque ----------
  async function iniciar() {
    var cfg = window.APP_CONFIG;
    if (!L.configValida(cfg) || !window.supabase || !window.supabase.createClient) {
      mostrarVista("vista-config");
      return;
    }
    db = window.supabase.createClient(cfg.SUPABASE_URL, cfg.SUPABASE_ANON_KEY);

    $("tab-login").addEventListener("click", function () { fijarModo("login"); });
    $("tab-registro").addEventListener("click", function () { fijarModo("registro"); });
    $("form-auth").addEventListener("submit", enviarAuth);
    $("btn-salir").addEventListener("click", salir);

    // Sondeo de sesión con una operación del contrato: sin sesión, rpc devuelve 42501.
    try {
      var sondeo = await db.rpc("cupos_disponibles", { p_taller_id: NIL_UUID });
      if (sondeo.error && (sondeo.error.code === "42501" || sondeo.error.status === 401)) {
        mostrarVista("vista-auth");
      } else if (sondeo.error) {
        mostrarVista("vista-auth");
        mostrarError("error-auth", L.traducirError(sondeo.error, "sondeo"));
      } else {
        await entrarApp(null);
      }
    } catch (e) {
      mostrarVista("vista-auth");
      mostrarError("error-auth", L.traducirError(e, "sondeo"));
    }
  }

  iniciar();
})();
