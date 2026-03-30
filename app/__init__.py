from flask import *
import os, json, sqlite3

app = Flask(__name__)

DB_NAME = "Data/database.db"
DB = sqlite3.connect(DB_NAME)
DBC = DB.cursor()

DBC.execute("CREATE TABLE IF NOT EXISTS games(name TEXT, reviews TEXT, description TEXT, user_rating INT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

DBC.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, reviews TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

DBC.execute("CREATE TABLE IF NOT EXISTS reviews(game_id INT, body TEXT, user_id INT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

@app.route("/")
def main():
    return "P04 Temp Site test"
    
if __name__ == "__main__":
    app.debug = True
    app.run()