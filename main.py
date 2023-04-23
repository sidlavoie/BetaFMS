from create_db import *
from config_net import *
from httpserver import *

httpPort = 8080
serverHostName = ''

init_db()
init_net("1234", "2345")
reset_net()
