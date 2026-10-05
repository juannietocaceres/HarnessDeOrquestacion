// Lógica pura (sin DOM ni red) para poder probarla con node.
(function (raiz) {
  "use strict";

  // Config válida: dos cadenas no vacías, URL http(s) y sin marcadores de plantilla.
  function configValida(cfg) {
    if (!cfg || typeof cfg.SUPABASE_URL !== "string" || typeof cfg.SUPABASE_ANON_KEY !== "string") return false;
    var url = cfg.SUPABASE_URL.trim();
    var key = cfg.SUPABASE_ANON_KEY.trim();
    if (!url || !key) return false;
    if (/^TU[-_]|<|>/i.test(url) || /^TU[-_]|<|>/i.test(key)) return false;
    return /^https?:\/\/[^\s/]+/i.test(url);
  }

  // Nombre: 1 a 100 caracteres sin espacios extremos (contrato).
  function validarNombre(valor) {
    var n = String(valor == null ? "" : valor).trim();
    if (!n) return { ok: false, mensaje: "Escribe tu nombre completo." };
    if (n.length > 100) return { ok: false, mensaje: "El nombre admite hasta 100 caracteres." };
    return { ok: true, valor: n };
  }

  // Traduce errores del proveedor a mensajes humanos (nunca muestra message crudo).
  function traducirError(error, contexto) {
    if (!error) return "";
    var code = String(error.code || error.error_code || "");
    var msg = String(error.message || "");
    if (contexto === "inscribir") {
      if (code === "23505") return "Ya estás inscrito en este taller.";
      if (code === "P0001" && /taller_lleno/.test(msg)) return "El taller ya no tiene cupos.";
      if (code === "23503") return "Ese taller ya no existe. Recarga la lista.";
      if (code === "23514") return "Revisa tu nombre: debe tener entre 1 y 100 caracteres.";
      if (code === "42501") return "Tu sesión expiró. Inicia sesión de nuevo.";
    }
    var porCodigo = {
      invalid_credentials: "Correo o contraseña incorrectos.",
      user_already_exists: "Ese correo ya tiene cuenta. Inicia sesión.",
      email_exists: "Ese correo ya tiene cuenta. Inicia sesión.",
      weak_password: "La contraseña es muy débil. Usa al menos 6 caracteres.",
      email_address_invalid: "El correo no es válido.",
      validation_failed: "Revisa el correo y la contraseña.",
      email_not_confirmed: "Confirma tu correo antes de iniciar sesión.",
      over_request_rate_limit: "Demasiados intentos. Espera un momento.",
      over_email_send_rate_limit: "Demasiados correos enviados. Espera un momento."
    };
    if (porCodigo[code]) return porCodigo[code];
    if (error.status === 401 || code === "42501") return "Inicia sesión para continuar.";
    if (/failed to fetch|network|load failed/i.test(msg) || error.name === "AuthRetryableFetchError") {
      return "No hay conexión con el servidor. Revisa tu internet.";
    }
    return "Algo salió mal. Intenta de nuevo.";
  }

  // Estado de un taller para la UI. cupos: entero o null (desconocido). inscrito: boolean.
  function estadoTaller(cupos, inscrito) {
    if (inscrito) return "inscrito";
    if (typeof cupos !== "number") return "desconocido";
    return cupos <= 0 ? "lleno" : "disponible";
  }

  function textoCupos(cupos) {
    if (typeof cupos !== "number") return "Cupos no disponibles";
    if (cupos <= 0) return "Sin cupos";
    return cupos === 1 ? "Queda 1 cupo" : "Quedan " + cupos + " cupos";
  }

  function formatearFecha(iso) {
    var d = new Date(iso);
    if (isNaN(d.getTime())) return "Fecha por confirmar";
    return d.toLocaleString("es-CO", { weekday: "long", day: "numeric", month: "long", hour: "numeric", minute: "2-digit" });
  }

  var api = { configValida: configValida, validarNombre: validarNombre, traducirError: traducirError, estadoTaller: estadoTaller, textoCupos: textoCupos, formatearFecha: formatearFecha };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else raiz.Logica = api;
})(typeof window !== "undefined" ? window : globalThis);
