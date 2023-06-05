from db_main import *
from config_net import *
from httpserver import *
from arena.dsConnection import *
from arena.driverStation import *
from arena.arena_main import *
from arena.sccCom import *

httpPort = 8080
serverHostName = ''

reset_db()
init_db()

#add_team("1234", "test1", "2023")
#add_team("5678", "test2", "2023")
#addMatch("1234", "5678")
#vert, jaune = loadNextMatch()
#sleep(10)
#end_match(vert, jaune)
test_scc = SCC(5001)
while True:
    test_scc.receiveStatus()
    print(test_scc.estopEnabled)
