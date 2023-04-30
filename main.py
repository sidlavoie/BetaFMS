from db_main import *
from config_net import *
from httpserver import *
from arena.dsConnection import *
from arena.driverStation import *

httpPort = 8080
serverHostName = ''

reset_db()
init_db()

add_team("1234", "test1", "2023")
add_team("5678", "test2", "2023")
#reset_net()
#init_net("1234", "5678")
vert = DriverStation('1234')
jaune = DriverStation('5678')
vert.dsIP, jaune.dsIP = discoverDS(vert.team_id, jaune.team_id)
print(vert.team_id, vert.dsIP)
print(jaune.team_id, jaune.dsIP)
