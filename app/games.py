import sqlite3

DB_NAME = "Data/database.db"

int get_id(game_name):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    DBC.execute("SELECT id FROM games WHERE name = ?;", (game_name, ))
    DBCF = DBC.fetchone()
    if DBCF is None:
        return -1
    DB.commit()
    DB.close()
    return DBCF[0]