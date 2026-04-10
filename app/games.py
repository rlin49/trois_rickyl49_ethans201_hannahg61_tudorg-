import sqlite3, reviews, users

DB_NAME = "Data/database.db"

def get_id(game_name): # TESTED
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    DBC.execute("SELECT id FROM games WHERE LOWER(name) LIKE LOWER(?);", (game_name, ))
    DBCF = DBC.fetchone()
    if DBCF is None:
        return None
    DB.commit()
    DB.close()
    return DBCF[0] - 1

def get_name(game_id): # TESTED
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    game_id+= 1;
    DBC.execute("SELECT name FROM games WHERE id = ?;", (game_id, ))
    DBCF = DBC.fetchone()
    if DBCF is None:
        return None
    DB.commit()
    DB.close()
    return DBCF[0]

def get_rating(game_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    if isinstance(game_info, int):
        DBC.execute("SELECT user_rating FROM games WHERE id = ?;", (game_info, ))
    else:
        DBC.execute("SELECT user_rating FROM games WHERE LOWER(name) LIKE LOWER(?);", (game_info, ))

    DBCF= DBC.fetchone()
    if DBCF[0] is None:
        return 0
    DB.commit()
    DB.close()
    return DBCF[0]

def get_num_ratings(game_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    if isinstance(game_info, int):
        DBC.execute("SELECT num_ratings FROM games WHERE id = ?;", (game_info, ))
    else:
        DBC.execute("SELECT num_ratings FROM games WHERE LOWER(name) LIKE LOWER(?);", (game_info, ))

    DBCF= DBC.fetchone()
    if DBCF[0] is None:
        return 0
    DB.commit()
    DB.close()
    return DBCF[0]



def add_rating(rating, game_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    num_ratings = get_num_ratings(game_info)
    user_rating = get_rating(game_info)
    total_rating = user_rating * num_ratings
    new_rating = (total_rating + rating)/(num_ratings + 1)
    new_num_ratings = num_ratings + 1

    if isinstance(game_info, int):
        DBC.execute("UPDATE games SET num_ratings = ? WHERE id = ?;", (new_num_ratings, game_info, ))
        DBC.execute("UPDATE games SET user_rating = ? WHERE id = ?;", (new_rating, game_info, ))
    else:
        DBC.execute("UPDATE games SET num_ratings = ? WHERE LOWER(name) LIKE LOWER(?);", (new_num_ratings, game_info, ))
        DBC.execute("UPDATE games SET user_rating = ? WHERE LOWER(name) LIKE LOWER(?)?;", (new_rating, game_info, ))

    DB.commit()
    DB.close()

def purge_ratings(game_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    if isinstance(game_info, int):
        DBC.execute("UPDATE games SET num_ratings = 0 WHERE id = ?;", (game_info, ))
        DBC.execute("UPDATE games SET user_rating = 0 WHERE id = ?;", (game_info, ))
    else:
        DBC.execute("UPDATE games SET num_ratings = 0 WHERE LOWER(name) LIKE LOWER(?);", (game_info, ))
        DBC.execute("UPDATE games SET user_rating = 0 LOWER(name) LIKE LOWER(?);", (game_info, ))

    DB.commit()
    DB.close()

def get_reviews(game_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    if isinstance(game_info, int):
        DBC.execute("SELECT reviews FROM games WHERE id = ?;", (game_info, ))
    else:
        DBC.execute("SELECT reviews FROM games WHERE LOWER(name) LIKE LOWER(?);", (game_info, ))

    DBCF = DBC.fetchone()
    if DBCF[0] is None:
        return ""
    DB.commit()
    DB.close()
    return DBCF[0]

def add_review(rev_id, game_info): # THIS EXISTS TO MAKE reviews.make_review() EASIER. PROB DON'T CALL THIS ON YOUR OWN
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    reviews = get_reviews(game_info)
    if reviews != "":
        reviews = reviews + f";{rev_id}"
    else:
        reviews = rev_id

    if isinstance(game_info, int):
        DBC.execute("UPDATE games SET reviews = ? WHERE id = ?;", (reviews, game_info, ))
    else:
        DBC.execute("UPDATE games SET reviews = ? WHERE LOWER(name) LIKE LOWER(?);", (reviews, game_info, ))

    DB.commit()
    DB.close()


def purge_reviews(game_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    if isinstance(game_info, int):
        DBC.execute("UPDATE games SET reviews = NULL WHERE id = ?;", (game_info, ))
    else:
        DBC.execute("UPDATE games SET reviews = NULL WHERE LOWER(name) LIKE LOWER(?);", (game_info, ))

    DB.commit()
    DB.close()
