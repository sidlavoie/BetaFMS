from create_db import *
from config_net import *
from httpserver import *

httpPort = 8080
serverHostName = "localhost"

run_server(serverHostName, httpPort)
init_db()
init_net("1010", "2020")
