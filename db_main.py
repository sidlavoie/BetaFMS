## This contains all the operations on the database
import sqlite3
import random
import string


def init_db():
    """ Initialises the database"""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS teams ("
                   "team_number VARCHAR(5), "
                   "team_name VARCHAR(50), "
                   "ranking_points INTEGER(3),"
                   "tournament_points INTEGER(3),"
                   "rookie_year VARCHAR(4), "
                   "ssid VARCHAR(8), "
                   "wpa_key VARCHAR(8))")

    cursor.execute("CREATE TABLE IF NOT EXISTS qual_matches ("
                   "id INTEGER PRIMARY KEY,"
                   "time DATETIME, "
                   "TEAM_VERT VARCHAR(5), "
                   "SUB_TEAM_VERT VARCHAR(8), "
                   "TEAM_JAUNE VARCHAR(5), "
                   "SUB_TEAM_JAUNE VARCHAR(8))")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS judge_awards ("
                   "id INTEGER PRIMARY KEY,"
                   "team_number VARCHAR(5),"
                   "award_name VARCHAR(50),"
                   "award_tournament_points INTEGER(3))")

    return 0



def reset_db():
    """ Drops all tables from the DB."""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS teams")
    cursor.execute("DROP TABLE IF EXISTS qual_matches")

def reset_qual_matches():
    """Deletes all qual matches"""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS qual_matches")
    cursor.execute("CREATE TABLE IF NOT EXISTS qual_matches ("
                   "id INTEGER PRIMARY KEY,"
                   "time DATETIME, "
                   "TEAM_VERT VARCHAR(5), "
                   "SUB_TEAM_VERT VARCHAR(8), "
                   "TEAM_JAUNE VARCHAR(5), "
                   "SUB_TEAM_JAUNE VARCHAR(8))")
    print("Table qual_matches was dropped per user-request!")
    return 0

def generate_ssid():
    """Generates a random SSID and WPA password for all teams"""
    randomSource = string.ascii_lowercase + string.digits
    ssid = ''.join(random.choice(randomSource) for i in range(8))
    wpa_key = ''.join(random.choice(randomSource) for i in range(8))
    return [ssid, wpa_key]


def regenerate_wpa(number):
    """Regenerates the WPA password and SSID of a specified team"""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    creds = generate_ssid()
    params = (creds[0], creds[1], number)
    cursor.execute("UPDATE teams SET ssid = ?, wpa_key = ? WHERE team_number = ?", params)
    print("Sucessfully regenerated WPA credentials for team %s with SSID %s and key %s" % (number, creds[0], creds[1]))
    connection.commit()



def add_team(number, name, rookie_year):
    """Add team and auto generate ssid and WPA key."""
    if len(number) > 5 or len(name) > 50 or len(rookie_year) != 4:
        raise Exception('Invalid team format - Number must be <= 5 digits and name <= 50 characters!')

    creds = generate_ssid()

    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()

    params = (number, name, rookie_year, creds[0], creds[1])
    cursor.execute("INSERT INTO teams (team_number, team_name, ranking_points, tournament_points, rookie_year, ssid, wpa_key) "
                   "VALUES (?, ?, 0, 0, ?, ?, ?)", params)
    connection.commit()
    print("Inserted team %s with ssid %s and WPA key %s" % (name, creds[0], creds[1]))


def getall_team(number):
    """Returns all infos from a specified team"""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM teams WHERE team_number = ?", [number])
    print(cursor.fetchone())
    return cursor.fetchall()[0]


def get_teamInfo(number):
    """Returns team without Wi-Fi infos"""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("SELECT team_number, team_name, rookie_year FROM teams WHERE team_number = ?", [number])
    return cursor.fetchall()[0]


def get_teamWifi(number):
    """Returns only team's Wi-Fi info"""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("SELECT ssid, wpa_key FROM teams WHERE team_number = ?", [number])
    return cursor.fetchall()[0]


def getTeamsTable():
    """Returns the whole team database"""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM teams")
    return cursor.fetchall()

def getTeamsNumberList():
    """Returns a list of all the teams numbers"""
    connection = sqlite3.connect("main.db")
    connection.row_factory = lambda cursor, row: row[0]
    c = connection.cursor()
    c.execute("SELECT team_number FROM teams")
    return c.fetchall()


def getMatchInfo(match_number):
    """Returns the infos for a specific match"""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("SELECT TEAM_VERT, TEAM_JAUNE, time FROM qual_matches "
                   "WHERE rowid = ?", [match_number])
    return cursor.fetchall()[0]


def addMatch(teamvert, subteamvert, teamjaune, subteamjaune, time):
    """Adds a match into the schedule"""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    params = (teamvert, subteamvert, teamjaune, subteamjaune, time)
    cursor.execute("INSERT INTO qual_matches (TEAM_VERT, SUB_TEAM_VERT, TEAM_JAUNE, SUB_TEAM_JAUNE, time) "
                   "VALUES (?, ?, ?, ?, ?)", params)
    connection.commit()

def addJudgeAward(award_name, award_tournament_points):
    """Adds a judged award in the judge_awards table. The judged awards must allocate a number of tournament points"""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    params = (award_name, award_tournament_points)
    cursor.execute("INSERT INTO judge_awards (award_name, award_tournament_points)"
                   "values (?,?)", params)
    connection.commit()

def allocateJudgeAward(award_name, team_number):
    """Adds a team to a previously inserted judged award"""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    params = (award_name, team_number)
    cursor.execute("INSERT INTO judge_awards (team_number)"
                   "values (?)" \
                   "WHERE award_name LIKE ?", params)
    connection.commit()

def getQualMatchTable():
    """Returns all the qualification matches"""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM qual_matches")
    return cursor.fetchall()

def deleteTeam(number):
    """Deletes the whole team's row from the database"""
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM teams WHERE team_number = ?", (number))
    connection.commit()
