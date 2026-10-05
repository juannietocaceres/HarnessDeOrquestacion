const test = require("node:test");
const assert = require("node:assert");
const L = require("../logic.js");

test("configValida: vacía, plantilla y válida", () => {
  assert.equal(L.configValida(undefined), false);
  assert.equal(L.configValida({ SUPABASE_URL: "", SUPABASE_ANON_KEY: "" }), false);
  assert.equal(L.configValida({ SUPABASE_URL: "TU-URL", SUPABASE_ANON_KEY: "x" }), false);
  assert.equal(L.configValida({ SUPABASE_URL: "https://abc.supabase.co", SUPABASE_ANON_KEY: "k" }), true);
});
test("validarNombre: vacío, solo espacios, largo, recorte", () => {
  assert.equal(L.validarNombre("   ").ok, false);
  assert.equal(L.validarNombre("a".repeat(101)).ok, false);
  assert.deepEqual(L.validarNombre("  Ana  "), { ok: true, valor: "Ana" });
});
test("traducirError: duplicado, cupo lleno, sesión, red, desconocido", () => {
  assert.match(L.traducirError({ code: "23505" }, "inscribir"), /Ya estás inscrito/);
  assert.match(L.traducirError({ code: "P0001", message: "taller_lleno" }, "inscribir"), /cupos/);
  assert.match(L.traducirError({ code: "42501" }, "inscribir"), /sesión/);
  assert.match(L.traducirError({ code: "invalid_credentials" }, "login"), /incorrectos/);
  assert.match(L.traducirError({ message: "Failed to fetch" }), /conexión/);
  assert.doesNotMatch(L.traducirError({ code: "XX", message: "secreto interno" }), /secreto/);
});
test("estadoTaller y textoCupos", () => {
  assert.equal(L.estadoTaller(0, false), "lleno");
  assert.equal(L.estadoTaller(0, true), "inscrito");
  assert.equal(L.estadoTaller(3, false), "disponible");
  assert.equal(L.estadoTaller(null, false), "desconocido");
  assert.equal(L.textoCupos(1), "Queda 1 cupo");
  assert.equal(L.textoCupos(0), "Sin cupos");
});
test("formatearFecha: inválida", () => {
  assert.equal(L.formatearFecha("nope"), "Fecha por confirmar");
});
