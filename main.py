from db_main import *
from config_net import *
from httpserver import *
from arena.dsConnection import *
from arena.driverStation import *
from arena.arena_main import *
from arena.sccCom import *
from schedule.scheduler import *
from schedule.insert import *
import tools.logger

httpPort = 8080
serverHostName = '0.0.0.0'

#tools.logger.setup_logging()

reset_db()
init_db()

add_team("296", "Northern Knights", "1999")
add_team("3544", "Spartiates", "2010")
add_team("6540", "Dynamo", "2017")
add_team("6622", "Stan Robotix", "2017")
add_team("6869", "Gladiateurs", "2018")
add_team("6872", "Panthera Ferro", "2022")
add_team("6929", "Cuivre & Or", "2018")
add_team("7700", "West Tech Paladins", "2019")
add_team("8067", "Alpha Lab", "2022")
add_team("9076", "Villaceraptors", "2023")


run_server(serverHostName, httpPort)



#reset_net()
#loadNextMatch()


#vert, jaune = loadNextMatch()
#sleep(10)
#end_match(vert, jaune)

