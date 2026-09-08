const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "../../plugins/adaptive-sdd/examples/habit-tracker");
const types = { ".css": "text/css", ".html": "text/html", ".js": "text/javascript", ".json": "application/json" };

http.createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname);
  const requested = pathname === "/" ? "index.html" : pathname.slice(1);
  const file = path.resolve(root, requested);
  if (!file.startsWith(root + path.sep) && file !== root) { response.writeHead(403).end(); return; }
  fs.readFile(file, (error, data) => {
    if (error) { response.writeHead(404).end("Not found"); return; }
    response.writeHead(200, { "Content-Type": types[path.extname(file)] || "application/octet-stream", "Cache-Control": "no-store" });
    response.end(data);
  });
}).listen(4173, "127.0.0.1", () => console.log("Habit tracker test server: http://127.0.0.1:4173"));
