import games, reviews, users, random, sqlite3, json

DB_NAME = "Data/database.db"

DB = sqlite3.connect(DB_NAME)
DBC = DB.cursor()

json_file = open("Data/games.json", "r")
data = json.load(json_file)
data_keys = list(data.keys())

for game in data_keys:
    DBC.execute("INSERT INTO games VALUES(?, NULL, NULL, NULL, NULL);", (game, ))
    DB.commit()

DBC.close()
