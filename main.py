from db_main import *
from config_net import *
from httpserver import *
from arena.dsConnection import *

httpPort = 8080
serverHostName = ''

reset_db()
init_db()

add_team("1234", "test1", "2023")
add_team("5678", "test2", "2023")
reset_net()
init_net("1234", "5678")
ds = discoverDS("1234", "5678")
print(ds)
input("Input to stop")
