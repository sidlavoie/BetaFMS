from http.server import *
import time

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<title>BetaFMS</title>", "utf-8"))
        self.wfile.write(bytes("<html><head>BetaFMS</head></html>", "utf-8"))


def run_server(hostname, port):
    webserver = HTTPServer((hostname, port), MyServer)
    print("Server started http://%s:%s" % (hostname, port))

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass

    webserver.server_close()
    print("Server stopped.")
