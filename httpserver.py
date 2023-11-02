import os
import cgi
import json
from http.server import *
import time
from schedule.insert import *
from schedule.scheduler import *
from db_main import getTeamsNumberList


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if self.path =='/':
            with open('www/index.html', 'r',encoding='utf-8') as html_file:
                html_content = html_file.read()

            self.wfile.write(bytes(html_content, "utf-8"))

        elif self.path =='/add_team?' or self.path == "/add_team":
            with open('www/add_team.html', 'r',encoding='utf-8') as html_file:
                html_content = html_file.read()

            self.wfile.write(bytes(html_content, "utf-8"))
            self.end_headers()

        elif self.path == '/scheduleControl' or self.path =='/scheduleControl?':
            with open('www/scheduleControl.html', 'r', encoding='utf-8') as html_file:
                html_content = html_file.read()

            self.wfile.write(bytes(html_content, "utf-8"))
            self.end_headers()

        else:
            self.send_response(404)
            with open('www/404.html', 'r',encoding='utf-8') as html_file:
                html_content = html_file.read()

            self.wfile.write(bytes(html_content, "utf-8"))
            self.end_headers()

    def do_POST(self):
        try:
            if self.path == '/generate_schedule':

                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'], }
                )
               
                starttime = form['startTime'].value

                ambreaktime = datetime(2023, 10, 15, 11, 2)
                lunchtime = datetime(2023, 10, 15, 12, 0)
                pmbreaktime = datetime(2023, 10, 15, 16, 0)
                cycletime = 10
                amduration = 10
                lunchduration = 60
                pmduration = 15
                (realambreak, reallunch, realpmbreak) = schedule_inserter( starttime, cycletime, ambreaktime,
                                                                          amduration, pmbreaktime, pmduration, lunchtime,
                                                                          lunchduration)
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()

            elif self.path == '/download_schedule':
                pdf_file = qual_schedule_exporter()

                self.send_response(200)
                self.send_header("Content-type", "application/pdf")
                self.send_header("Content-Disposition", f"attachment; filename={pdf_file}")
                self.end_headers()

                with open(pdf_file, 'rb') as pdf:
                    self.wfile.write(pdf.read())

            elif self.path == '/teamadd':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'], }
                )
                if 'numEqui' in form and 'nomEq' in form and 'rookie' in form:
                    numEqui = form['numEqui'].value
                    nomEq = form['nomEq'].value
                    rookie = form['rookie'].value
                    if len(numEqui) <= 5 and len(nomEq) <= 50 and len(rookie) <= 4:
                        add_team(numEqui, nomEq, rookie)
                        self.send_response(302)
                        self.send_header("Location", "/add_team")
                        self.end_headers()
                    else:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps("Nombre de symboles trop grand dans un des champs!").encode('utf-8'))

                else:
                    self.send_response(500)
                    self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            error_message = str(e)
            response = {'error': error_message}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))


def run_server(hostname, port):
    webserver = HTTPServer((hostname, port), MyServer)
    print("Server started http://%s:%s" % (hostname, port))

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass

    webserver.server_close()
    print("Server stopped.")
