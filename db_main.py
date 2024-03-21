# This contains all the operations on the database
import sqlite3
import random
import string


def init_db():
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS teams ("
                   "team_number VARCHAR(5), "
                   "team_name VARCHAR(50), "
                   "ranking_points INTEGER(3),"
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
    return 0


# Drops all tables from the DB.
def reset_db():
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS teams")
    cursor.execute("DROP TABLE IF EXISTS qual_matches")

def reset_qual_matches():
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
    randomSource = string.ascii_lowercase + string.digits
    ssid = ''.join(random.choice(randomSource) for i in range(8))
    wpa_key = ''.join(random.choice(randomSource) for i in range(8))
    return [ssid, wpa_key]


def regenerate_wpa(number):
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    creds = generate_ssid()
    params = (creds[0], creds[1], number)
    cursor.execute("UPDATE teams SET ssid = ?, wpa_key = ? WHERE team_number = ?", params)
    print("Sucessfully regenerated WPA credentials for team %s with SSID %s and key %s" % (number, creds[0], creds[1]))
    connection.commit()


# Add team and auto generate ssid and WPA key.
def add_team(number, name, rookie_year):

    if len(number) > 5 or len(name) > 50 or len(rookie_year) != 4:
        raise Exception('Invalid team format - Number must be <= 5 digits and name <= 50 characters!')

    creds = generate_ssid()

    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()

    params = (number, name, rookie_year, creds[0], creds[1])
    cursor.execute("INSERT INTO teams (team_number, team_name, ranking_points, rookie_year, ssid, wpa_key) "
                   "VALUES (?, ?, 0, ?, ?, ?)", params)
    connection.commit()
    print("Inserted team %s with ssid %s and WPA key %s" % (name, creds[0], creds[1]))


# Get all infos from a specified team
def getall_team(number):
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM teams WHERE team_number = ?", [number])
    print(cursor.fetchone())
    return cursor.fetchall()[0]


# Get team without Wi-Fi infos
def get_teamInfo(number):
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("SELECT team_number, team_name, rookie_year FROM teams WHERE team_number = ?", [number])
    return cursor.fetchall()[0]


def get_teamWifi(number):
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("SELECT ssid, wpa_key FROM teams WHERE team_number = ?", [number])
    return cursor.fetchall()[0]


def getTeamsTable():
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM teams")
    return cursor.fetchall()


# Returns a list of all the teams numbers
def getTeamsNumberList():
    connection = sqlite3.connect("main.db")
    connection.row_factory = lambda cursor, row: row[0]
    c = connection.cursor()
    c.execute("SELECT team_number FROM teams")
    return c.fetchall()


def getMatchInfo(match_number):
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("SELECT TEAM_VERT, TEAM_JAUNE, time FROM qual_matches "
                   "WHERE rowid = ?", [match_number])
    return cursor.fetchall()[0]


def addMatch(teamvert, subteamvert, teamjaune, subteamjaune, time):
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    params = (teamvert, subteamvert, teamjaune, subteamjaune, time)
    cursor.execute("INSERT INTO qual_matches (TEAM_VERT, SUB_TEAM_VERT, TEAM_JAUNE, SUB_TEAM_JAUNE, time) "
                   "VALUES (?, ?, ?, ?, ?)", params)
    connection.commit()


def getQualMatchTable():
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM qual_matches")
    return cursor.fetchall()

def deleteTeam(number):
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM teams WHERE team_number = ?", (number,))
    connection.commit()
