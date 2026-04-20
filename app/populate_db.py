import games, reviews, users, random, sqlite3, json

DB_NAME = "Data/database.db"

DB_NAME = "Data/database.db"
DB = sqlite3.connect(DB_NAME)
DBC = DB.cursor()

DBC.execute("CREATE TABLE IF NOT EXISTS games(name TEXT, reviews TEXT, user_rating INT, num_ratings INT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

# DBC.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, reviews TEXT, bio TEXT, favorites TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")
#
# DBC.execute("CREATE TABLE IF NOT EXISTS reviews(game_id INT, body TEXT, user_id INT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

DB = sqlite3.connect(DB_NAME)
DBC = DB.cursor()

json_file = open("Data/games.json", "r")
data = json.load(json_file)
data_keys = list(data.keys())

for game in data_keys:
    DBC.execute("INSERT INTO games VALUES(?, NULL, NULL, NULL, NULL);", (game, ))
    DB.commit()

DBC.close()
