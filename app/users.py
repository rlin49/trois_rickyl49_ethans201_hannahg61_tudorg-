import sqlite3, games, reviews

DB_NAME = "Data/database.db"

def get_id(username):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    DBC.execute("SELECT id FROM users WHERE LOWER(name) LIKE LOWER(?);", (username, ))
    DBCF = DBC.fetchone()
    if DBCF is None:
        return None
    DB.commit()
    DB.close()
    return DBCF[0]
    
def get_reviews(user_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()
    
    if isinstance(user_info, int):
        DBC.execute("SELECT reviews FROM users WHERE id = ?;", (user_info, ))
    else:
        DBC.execute("SELECT reviews FROM users WHERE LOWER(username) LIKE LOWER(?);", (user_info, ))
        
    DBCF = DBC.fetchone()
    if DBCF[0] is None:
        return ""
    DB.commit()
    DB.close()
    return DBCF[0]
    
def add_review(rev_id, user_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()
    
    reviews = get_reviews(user_info)
    if reviews != "":
        reviews = reviews + f";{rev_id}"
    else:
        reviews = rev_id
    
    if isinstance(game_info, int):
        DBC.execute("UPDATE users SET reviews = ? WHERE id = ?;", (reviews, _info, ))
    else:
        DBC.execute("UPDATE users SET reviews = ? WHERE LOWER(username) LIKE LOWER(?);", (reviews, user_info, ))
    
    DB.commit()
    DB.close()