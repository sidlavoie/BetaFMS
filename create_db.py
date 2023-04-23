import sqlite3


def init_db():
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE TABLE teams ("
                       "team_number VARCHAR(5), "
                       "team_name VARCHAR(50), "
                       "rookie_year VARCHAR(4))")
    except sqlite3.OperationalError:
        print("Table Teams exists")
    try:
        cursor.execute("CREATE TABLE qual_matches ("
                       "time DATETIME, "
                       "TEAM1 VARCHAR(5), "
                       "TEAM2 VARCHAR(5))")
    except sqlite3.OperationalError:
        print("Table qual_matches exists")
    # test

    cursor.execute("INSERT INTO teams VALUES (0001, 'TEST1', 2023), (0002, 'TEST2', 2023), (0003, 'TEST3', 2023)")
    i = cursor.execute("SELECT * FROM teams")
    print(i.fetchall())
