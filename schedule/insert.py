from db_main import addMatch


def schedule_inserter(schedule):
    for i in range(len(schedule)):
        for j in range(2):
            vert = schedule[i][j][0].split(" ")
            jaune = schedule[i][j][1].split(" ")
            addMatch(vert[0], vert[1], jaune[0], jaune[1])
