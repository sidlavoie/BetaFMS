from db_main import *
from config_net import *
from httpserver import *

httpPort = 8080
serverHostName = ''

reset_db()
init_db()

add_team("1234", "test1", "2023")
add_team("4678", "test2", "2023")

init_net("1234", "4678")
regenerate_wpa('1234')
input("Waiting...")
reset_net()
init_net("1234", "4678")
input("Waiting 2...")

reset_net()
