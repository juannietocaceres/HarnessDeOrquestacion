// Genera config.js a partir de un archivo .env (por defecto .env.local o .env en la carpeta del proyecto).
// Uso: node scripts/generar-config.js [ruta-al-env]
// Solo lee SUPABASE_URL y SUPABASE_ANON_KEY (valores públicos del cliente).
const fs = require("fs");
const path = require("path");

const raiz = path.join(__dirname, "..");
const candidatos = process.argv[2]
  ? [path.resolve(process.argv[2])]
  : [path.join(raiz, ".env.local"), path.join(raiz, ".env")];
const origen = candidatos.find((p) => fs.existsSync(p));
if (!origen) {
  console.error("No encuentro un .env. Copia .env.example a .env y complétalo.");
  process.exit(1);
}
const valores = {};
for (const linea of fs.readFileSync(origen, "utf8").split(/\r?\n/)) {
  const m = linea.match(/^\s*([A-Z_]+)\s*=\s*(.*?)\s*$/);
  if (m) valores[m[1]] = m[2].replace(/^["']|["']$/g, "");
}
for (const k of ["SUPABASE_URL", "SUPABASE_ANON_KEY"]) {
  if (!valores[k]) {
    console.error("Falta " + k + " en " + origen);
    process.exit(1);
  }
}
const salida =
  "// Generado por scripts/generar-config.js. No commitear.\n" +
  "window.APP_CONFIG = " +
  JSON.stringify({ SUPABASE_URL: valores.SUPABASE_URL, SUPABASE_ANON_KEY: valores.SUPABASE_ANON_KEY }, null, 2) +
  ";\n";
fs.writeFileSync(path.join(raiz, "config.js"), salida);
console.log("config.js generado desde " + origen);
