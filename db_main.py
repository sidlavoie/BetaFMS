import sqlite3
import random
import string


def init_db():
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS teams ("
                   "team_number VARCHAR(5), "
                   "team_name VARCHAR(50), "
                   "rookie_year VARCHAR(4), "
                   "ssid VARCHAR(8), "
                   "wpa_key VARCHAR(8))")

    cursor.execute("CREATE TABLE IF NOT EXISTS qual_matches ("
                   "time DATETIME, "
                   "TEAM1 VARCHAR(5), "
                   "TEAM2 VARCHAR(5))")
    return 0


# Drops all tables from the DB.
def reset_db():
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE teams")
    cursor.execute("DROP TABLE qual_matches")

# Add team and auto generate ssid and WPA key.
def add_team(number, name, rookie_year):

    if len(number) > 5 or len(name) > 50 or len(rookie_year) != 4:
        raise Exception('Invalid team format - Number must be <= 5 digits and name <= 50 characters!')

    randomSource = string.ascii_lowercase + string.digits
    ssid = ''.join(random.choice(randomSource) for i in range(8))
    wpa_key = ''.join(random.choice(randomSource) for i in range(8))

    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()

    params = (number, name, rookie_year, ssid, wpa_key)
    cursor.execute("INSERT INTO teams (team_number, team_name, rookie_year, ssid, wpa_key) "
                   "VALUES (?, ?, ?, ?, ?)", params)
    connection.commit()
    print("Inserted team %s with ssid %s and WPA key %s" % (name, ssid, wpa_key))


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
