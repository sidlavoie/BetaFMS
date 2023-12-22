import random

def generate_schedule(teams, subteam_colors):
    colors = subteam_colors
    if len(teams) > 12:
        raise ValueError("There must be no more than 12 teams")

    random.shuffle(teams)

    if len(teams) % 2 != 0:
        teams.append('surrogate')

    # if there is more than 9 teams, there will need to be a fifth round so red will replay
    # For 11 or 12 teams, a sixth round is added
    if 9 < len(teams) < 11 and len(colors) < 5:
        colors.append(colors[0])
    if len(teams) > 11 and len(colors) < 6:
        colors.append(colors[1])
    # Generate a round-robin schedule
    num_teams = len(teams)
    schedule = []
    surrogates_list = []

    for _ in range(len(colors)):
        round_schedule = []

        # Pair up the teams for the current round, ensuring alternating sides
        for i in range(num_teams // 2):
            if _ % 2 == 0:
                match = [teams[i] + ' ' + colors[_], teams[num_teams - 1 - i] + ' ' + colors[_]]
            else:
                match = [teams[num_teams - 1 - i] + ' ' + colors[_], teams[i] + ' ' + colors[_]]
            round_schedule.append(match)

        # Assigns surrogate team, if any
        for ma in range(len(round_schedule)):
            for te in range(len(round_schedule[ma])):
                if 'surrogate' in round_schedule[ma][te]:
                    while True:
                        randomTeam = random.choice(teams)
                        if randomTeam not in surrogates_list and randomTeam != 'surrogate':
                            surrogates_list.append(randomTeam)
                            round_schedule[ma][te] = randomTeam + ' ' + colors[_] + ' S'
                            break

            # Reorganize the schedule so that teams ideally do not play consecutive matches
        for i in range(len(round_schedule) - 1):
            common_teams = set(round_schedule[i])
            found_match = next((match for match in round_schedule[i + 1:] if not set(match).intersection(common_teams)), None)
            if found_match:
                round_schedule.remove(found_match)
                round_schedule.insert(i + 1, found_match)

        schedule.append(round_schedule)

        # Rotate the teams for the next round
        teams.insert(1, teams.pop())
    return schedule


def printSchedule(schedule):
    for round_num, round_schedule in enumerate(schedule, start=1):
        print(f"Round {round_num}:")
        for match_num, match in enumerate(round_schedule, start=1):
            print(f"Match {match_num}: {match[0]} vs {match[1]}")
        print()


# Used for testing purposes, will need to be reimplemented
def check_number_matches(schedule):
    my_dict = {}
    for i in range(len(schedule)):
        for j in range(len(schedule[i])):
            for k in range(len(schedule[i][j])):
                key = schedule[i][j][k][5]
                if key not in my_dict.keys():
                    my_dict[key] = 1
                else:
                    my_dict[key] += 1
    return my_dict


