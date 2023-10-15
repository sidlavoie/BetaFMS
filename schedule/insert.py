from db_main import addMatch


def schedule_inserter(schedule, start_time, cycle_time, am_break_time, am_break_duration, pm_break_time, pm_break_duration, lunch_time, lunch_duration):
    #This inserts matches into the schedule
    for i in range(len(schedule)):
        for j in range(2):
            vert = schedule[i][j][0].split(" ")
            jaune = schedule[i][j][1].split(" ")
            addMatch(vert[0], vert[1], jaune[0], jaune[1])
