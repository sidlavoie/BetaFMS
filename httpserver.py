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
        try:
            self.send_response(200)
            #self.send_header("Content-type", "text/html")
            self.end_headers()

            if self.path =='/' or self.path =="/?":
                with open('www/index.html', 'r',encoding='utf-8') as html_file:
                    html_content = html_file.read()

                self.wfile.write(bytes(html_content, "utf-8"))
                return

            elif self.path == '/favicon.ico':
                with open('www/static/images/favicon.ico', 'rb') as favicon_file:
                    favicon_content = favicon_file.read()

                self.send_response(200)
                self.send_header("Content-type", "image/x-icon")
                self.send_header("Content-Length", str(len(favicon_content)))
                self.wfile.write(favicon_content)
                self.end_headers()
                return

            elif self.path.startswith("/add_team"):
                template = env.get_template("www/add_team.html")

                 # Example team data
                teams = getTeamsTable()

                rendered_template = template.render(teams=teams)

                self.wfile.write(rendered_template.encode('utf-8'))
                self.end_headers()
                return

            elif self.path.startswith('/scheduleControl'):
                template = env.get_template("www/scheduleControl.html")

                rendered_template = template.render(
                    day=schedule_conf.day.strftime("%Y-%m-%d"),
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
                return

            else:
                try:  # Handle media content and static pages (pictures, sounds, scripts...)
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

                        return

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

                        return

                    if self.path.find(".css") != -1:  # Handle css
                        if self.path[0] == '/':
                            self.path = self.path[1:]
                        if self.path.find("www/css/") == -1:
                            self.path = "www/css/" + self.path

                        with open(self.path, 'rb') as css_file:
                            css_content = css_file.read()

                        self.send_response(200)
                        self.send_header("Content-type", "text/css")
                        self.send_header("Content-Length", str(len(css_content)))
                        self.wfile.write(css_content)
                        self.end_headers()

                        return

                    if self.path.find(".js") != -1:  # Handle JS
                        if self.path[0] == '/':
                            self.path = self.path[1:]
                        if self.path.find("www/scripts/") == -1:
                            self.path = "www/scripts/" + self.path

                        with open(self.path, 'rb') as js_file:
                            js_content = js_file.read()

                        self.send_response(200)
                        self.send_header("Content-type", "application/javascript")
                        self.send_header("Content-Length", str(len(js_content)))
                        self.wfile.write(js_content)
                        self.end_headers()

                        return

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

        except Exception as e:
            self.handle_error(500, str(e))

    def do_POST(self):
        try:
            if self.path == '/generate_schedule':

                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'], }
                )

                # Retrieve form values
                day_str = form.getvalue('day')
                starttime_str = datetime.strptime(form.getvalue('starttime'), '%H:%M').time()
                ambreaktime_str = datetime.strptime(form.getvalue('ambreaktime'), '%H:%M').time()
                lunchtime_str = datetime.strptime(form.getvalue('lunchtime'), '%H:%M').time()
                pmbreaktime_str = datetime.strptime(form.getvalue('pmbreaktime'), '%H:%M').time()

                # Convert string values to datetime objects and insert them in the config class
                schedule_conf.day = datetime(int(day_str[0:4]), int(day_str[5:7]), int(day_str[8:10]))
                schedule_conf.starttime = datetime.combine(schedule_conf.day, starttime_str)
                schedule_conf.ambreaktime = datetime.combine(schedule_conf.day, ambreaktime_str)
                schedule_conf.lunchtime = datetime.combine(schedule_conf.day, lunchtime_str)
                schedule_conf.pmbreaktime = datetime.combine(schedule_conf.day, pmbreaktime_str)
                schedule_conf.cycletime = int(form.getvalue('cycletime'))
                schedule_conf.amduration = int(form.getvalue('amduration'))
                schedule_conf.lunchduration = int(form.getvalue('lunchduration'))
                schedule_conf.pmduration = int(form.getvalue('pmduration'))

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
                        self.send_header("Location", "/add_team?")
                        self.end_headers()
                    else:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps("Nombre de symboles trop grand dans un des champs!").encode('utf-8'))

            elif self.path == '/removeteam':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'], }
                )

                # Retrieve form values
                deleteTeam(form.getvalue("delteam"))
                self.send_response(302)
                self.send_header("Location", "/add_team?")
                self.end_headers()

            elif self.path == '/wparegen':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'], }
                )

                # Retrieve form values
                regenerate_wpa(form.getvalue("wpateam"))
                self.send_response(302)
                self.send_header("Location", "/add_team?")
                self.end_headers()
            
            else:
                self.send_response(404)
                self.end_headers()

        except Exception as e:
            self.handle_error(500, str(e))

    def handle_error(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Serve the error page directly
        with open('www/error.html', 'r', encoding='utf-8') as error_page_file:
            error_page_content = error_page_file.read()

        # Replace the placeholder with the actual error message
        error_page_content = error_page_content.replace('{{errorMessage}}', message)

        self.wfile.write(bytes(error_page_content, 'utf-8'))


def run_server(hostname, port):
    webserver = HTTPServer((hostname, port), MyServer)
    print("Server started http://%s:%s" % (hostname, port))

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        webserver.RequestHandlerClass.handle_error(webserver.RequestHandlerClass, 500, str(e))


    webserver.server_close()
    print("Server stopped.")
