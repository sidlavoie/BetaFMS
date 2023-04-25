from db_main import *
from config_net import *
from httpserver import *

httpPort = 8080
serverHostName = ''

reset_db()
init_db()

add_team("1234", "test1", "2023")
add_team("4678", "test2", "2023")
test = get_teamWifi('1234')

init_net("1234", "4678")
allo = input("Press any key to unconfigure")
reset_net()
reset_ap()

