import os
import cgi
import json
from http.server import *
import time
from jinja2 import Environment, FileSystemLoader

# Custom modules
from arena.arena_main import *
from schedule.insert import *
from schedule.scheduler import *
from db_main import getTeamsNumberList

env = Environment(loader=FileSystemLoader('.'))
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if self.path =='/':
            with open('www/index.html', 'r',encoding='utf-8') as html_file:
                html_content = html_file.read()

            self.wfile.write(bytes(html_content, "utf-8"))

        elif self.path == '/favicon.ico':
            with open('www/static/images/favicon.ico', 'rb') as favicon_file:
                favicon_content = favicon_file.read()

            self.send_response(200)
            self.send_header("Content-type", "image/x-icon")
            self.send_header("Content-Length", str(len(favicon_content)))
            self.wfile.write(favicon_content)
            self.end_headers()

        elif self.path == '/add_team?':
            with open('www/add_team.html', 'r', encoding='utf-8') as html_file:
                html_content = html_file.read()

            self.wfile.write(bytes(html_content, "utf-8"))
            self.end_headers()

        elif self.path == '/scheduleControl?':
            template = env.get_template("www/scheduleControl.html")

            rendered_template = template.render(
                day=f"{schedule_conf.day.year}-{schedule_conf.day.month}-{schedule_conf.day.day}",
                starttime=schedule_conf.starttime.strftime('%H:%M'),
                ambreaktime=schedule_conf.ambreaktime.strftime('%H:%M'),
                lunchtime=schedule_conf.lunchtime.strftime('%H:%M'),
                pmbreaktime=schedule_conf.pmbreaktime.strftime('%H:%M'),
                cycletime=schedule_conf.cycletime,
                amduration=schedule_conf.amduration,
                lunchduration=schedule_conf.lunchduration,
                pmduration=schedule_conf.pmduration
            )

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.wfile.write(rendered_template.encode('utf-8'))
            self.end_headers()

        else:
            try:
                if self.path.find(".jpeg") != -1:  # Handle pictures
                    if self.path[0] == '/':
                        self.path = self.path[1:]
                    if self.path.find("www/static/images/") == -1:
                        self.path = "www/static/images/" + self.path

                    with open(self.path, 'rb') as image_file:
                        image_content = image_file.read()

                    self.send_response(200)
                    self.send_header("Content-type", "image/x-icon")
                    self.send_header("Content-Length", str(len(image_content)))
                    self.wfile.write(image_content)
                    self.end_headers()

                if self.path.find(".wav") != -1:  # Handle audio
                    if self.path[0] == '/':
                        self.path = self.path[1:]
                    if self.path.find("www/static/audio/") == -1:
                        self.path = "www/static/audio/" + self.path

                    with open(self.path, 'rb') as audio_file:
                        audio_content = audio_file.read()

                    self.send_response(200)
                    self.send_header("Content-type", "audio/wav")
                    self.send_header("Content-Length", str(len(audio_content)))
                    self.wfile.write(audio_content)
                    self.end_headers()

                else:
                    # Append www and .html if it does not exist
                    if self.path.find('www',1) == -1:
                        self.path = "www" + self.path
                    if self.path.find(".html") == -1:
                        self.path = self.path + ".html"

                    with open(self.path, 'r', encoding='utf-8')as html_file:  # just return the name of the file
                        html_content = html_file.read()

                    self.wfile.write(bytes(html_content, "utf-8"))
                    self.end_headers()

            except FileNotFoundError:  # 404 if it does not exist
                print("404")
                self.send_response(404)
                with open('www/404.html', 'r', encoding='utf-8') as html_file:
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

                # Retrieve form values
                #day_str = form.getvalue('day')
                starttime_str = form.getvalue('starttime')
                ambreaktime_str = form.getvalue('ambreaktime')
                lunchtime_str = form.getvalue('lunchtime')
                pmbreaktime_str = form.getvalue('pmbreaktime')

                # Convert string values to datetime objects
                #schedule_conf.day = datetime.strptime(day_str, '%Y:%m:%d')
                schedule_conf.starttime = datetime.strptime(starttime_str, '%H:%M')
                schedule_conf.ambreaktime = datetime.strptime(ambreaktime_str, '%H:%M')
                schedule_conf.lunchtime = datetime.strptime(lunchtime_str, '%H:%M')
                schedule_conf.pmbreaktime = datetime.strptime(pmbreaktime_str, '%H:%M')

                (realambreak, reallunch, realpmbreak) = schedule_inserter(schedule_conf.starttime, schedule_conf.cycletime, schedule_conf.ambreaktime,
                                                                          schedule_conf.amduration, schedule_conf.pmbreaktime, schedule_conf.pmduration, schedule_conf.lunchtime,
                                                                          schedule_conf.lunchduration)
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

            elif self.path == '/loadnextmatch':
                loadNextMatch()

                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()

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
