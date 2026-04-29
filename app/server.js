const http = require('http');
const requestListener = function (req, res) {
  res.writeHead(200);
  res.end('¡Logrado! Servidor Node.js activo en GKE.');
}
const server = http.createServer(requestListener);
server.listen(8080, '0.0.0.0', () => {
  console.log('Servidor escuchando en el puerto 8080');
});
