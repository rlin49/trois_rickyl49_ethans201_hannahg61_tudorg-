import sqlite3

DB_NAME = "Data/database.db"

def get_id(game_name): # TESTED
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    DBC.execute("SELECT id FROM games WHERE LOWER(name) LIKE LOWER(?);", (game_name, ))
    DBCF = DBC.fetchone()
    if DBCF is None:
        return -1
    DB.commit()
    DB.close()
    return DBCF[0]
    
def get_name(game_id): # TESTED
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()
    
    DBC.execute("SELECT name FROM games WHERE id = ?;", (game_id, ))
    DBCF = DBC.fetchone()
    if DBCF is None:
        return -1
    DB.commit()
    DB.close()
    return DBCF[0]
    
def get_rating(game_info):
    DB = sqlite3.connect(DB_NAME)
    DBC= DB.cursor()
    
    if isInstance(game_info, int):
        DBC.execute("SELECT user_rating FROM games WHERE id = ?;", (game_info, ))
    else:
        DBC.execute("SELECT user_rating FROM games WHERE name = ?;", (game_info, ))
        
    DBCF= DBC.fetchone()
    if DBCF is None:
        return -1
    DB.commit()
    DB.close()
    return DBCF[0]
    
def add_rating(game_info):
    DB = sqlite3.connect(DB_NAME)
    DBC= DB.cursor()
    
    
    