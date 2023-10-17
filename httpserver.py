import os
from http.server import *
import time
from schedule.insert import *
from schedule.scheduler import *
from db_main import getTeamsNumberList

# NE FONCTIONNE PAS ENCORE!!!!!!!
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path =='/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open('www/index.html', 'r',encoding='utf-8') as html_file:
                html_content = html_file.read()

            self.wfile.write(bytes(html_content, "utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/generate_schedule':
            test = getTeamsNumberList()
            colors = ["Rouge", "Bleu", "Violet", "Orange"]
            schedule = generate_schedule(test, colors)
            printSchedule(schedule)
            starttime = datetime(2023, 10, 15, 10, 30)
            ambreaktime = datetime(2023, 10, 15, 11, 2)
            lunchtime = datetime(2023, 10, 15, 12, 0)
            pmbreaktime = datetime(2023, 10, 15, 16, 0)
            cycletime = 10
            amduration = 10
            lunchduration = 60
            pmduration = 15
            (realambreak, reallunch, realpmbreak) = schedule_inserter(schedule, starttime, cycletime, ambreaktime,
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
        else:
            self.send_response(404)
            self.end_headers()




def run_server(hostname, port):
    webserver = HTTPServer((hostname, port), MyServer)
    print("Server started http://%s:%s" % (hostname, port))

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass

    webserver.server_close()
    print("Server stopped.")
