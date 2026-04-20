import sqlite3, games, reviews

DB_NAME = "Data/database.db"

def get_id(username):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    DBC.execute("SELECT id FROM users WHERE LOWER(username) LIKE LOWER(?);", (username, ))
    DBCF = DBC.fetchone()
    if DBCF is None:
        return None
    DB.commit()
    DB.close()
    return DBCF[0]

def get_username(user_id):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    DBC.execute("SELECT username FROM users WHERE id = ?;", (user_id, ))
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
    if DBCF is None:
        return ""
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

    print(reviews)
    if isinstance(user_info, int):
        DBC.execute("UPDATE users SET reviews = ? WHERE id = ?;", (reviews, user_info, ))
    else:
        DBC.execute("UPDATE users SET reviews = ? WHERE LOWER(username) LIKE LOWER(?);", (reviews, user_info, ))

    DB.commit()
    DB.close()

def purge_reviews(user_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    if isinstance(user_info, int):
        DBC.execute("UPDATE users SET reviews = NULL WHERE id = ?;", (user_info, ))
    else:
        DBC.execute("UPDATE users SET reviews = NULL WHERE LOWER(username) LIKE LOWER(?);", (user_info, ))

    DB.commit()
    DB.close()

def update_bio(bio, user_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    if isinstance(user_info, int):
        DBC.execute("UPDATE users SET bio = ? WHERE id = ?;", (bio, user_info, ))
    else:
        DBC.execute("UPDATE users SET bio = ? WHERE LOWER(username) LIKE LOWER(?);", (bio, user_info, ))

    DB.commit()
    DB.close()

def get_bio(user_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    if isinstance(user_info, int):
        DBC.execute("SELECT bio FROM users WHERE id = ?;", (user_info, ))
    else:
        DBC.execute("SELECT bio FROM users WHERE LOWER(username) LIKE LOWER(?);", (user_info, ))

    DBCF = DBC.fetchone()

    if DBCF is None:
        return ""
    if DBCF[0] is None:
        return ""
    DB.commit()
    DB.close()
    return DBCF[0]

def get_favorites(user_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    if isinstance(user_info, int):
        DBC.execute("SELECT favorites FROM users WHERE id = ?;", (user_info, ))
    else:
        DBC.execute("SELECT favorites FROM users WHERE LOWER(username) LIKE LOWER(?);", (user_info, ))

    DBCF = DBC.fetchone()
    if DBCF is None:
        return ""
    if DBCF[0] is None:
        return ""
    DB.commit()
    DB.close()
    return DBCF[0]

def add_favorite(fav_id, user_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()



    favorites = get_favorites(user_info)

    fav_arr = favorites.split(";")
    if fav_id in favorites:
        return

    if favorites != "":
        favorites = favorites + f";{fav_id}"
    else:
        favorites = fav_id

    print("Favorites bruv: " + favorites)



    if isinstance(user_info, int):
        DBC.execute("UPDATE users SET favorites = ? WHERE id = ?;", (favorites, user_info, ))
    else:
        DBC.execute("UPDATE users SET favorites = ? WHERE LOWER(username) LIKE LOWER(?);", (favorites, user_info, ))

    DB.commit()
    DB.close()

def remove_favorite(fav_id, user_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    favorites = get_favorites(user_info)
    if favorites == "":
        return

    fav_arr = favorites.split(";")
    if fav_id in fav_arr:
        fav_arr.remove(fav_id)
    else:
        return

    new_favorites = ";".join(fav_arr)
    if isinstance(user_info, int):
        DBC.execute("UPDATE users SET favorites = ? WHERE id = ?;", (new_favorites, user_info, ))
    else:
        DBC.execute("UPDATE users SET favorites = ? WHERE LOWER(username) LIKE LOWER(?);", (new_favorites, user_info, ))

    DB.commit()
    DB.close()

def is_favorite(fav_id, user_info):
    favorites = get_favorites(user_info)
    if favorites == "":
        return False

    fav_arr = favorites.split(";")
    if fav_id in fav_arr:
        return True
    return False
