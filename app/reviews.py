import sqlite3, games, users

DB_NAME = "Data/database.db"

def make_review(review_text, user_info, game_info):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    if not isinstance(user_info, int):
        user_info = users.get_id(user_info)

    if not isinstance(game_info, int):
        game_info = games.get_id(game_info)

    DBC.execute("INSERT INTO reviews VALUES(?, ?, ?, NULL);", (game_info, review_text, user_info, ))
    DB.commit()


    # adding to user & game
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    DBC.execute("SELECT id FROM reviews WHERE body = ?;", (review_text, ))
    DBCF = DBC.fetchone()

    rev_id = DBCF[0]

    games.add_review(rev_id, game_info)
    users.add_review(rev_id, user_info)
    DB.commit()
    DB.close()


def get_review(rev_id):
    DB = sqlite3.connect(DB_NAME)
    DBC = DB.cursor()

    DBC.execute("SELECT body FROM reviews WHERE id = ?;", (rev_id, ))
    DBCF = DBC.fetchone()
    if DBCF[0] is None:
        return ""
    DB.commit()
    DB.close()
    return DBCF[0]
