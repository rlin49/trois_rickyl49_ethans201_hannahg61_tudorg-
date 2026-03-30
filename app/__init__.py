from flask import *
import os, json, sqlite3

app = Flask(__name__)

DB_NAME = "Data/database.db"
DB = sqlite3.connect(DB_NAME)
DBC = DB.cursor()

DBC.execute("CREATE TABLE IF NOT EXISTS games(name TEXT, reviews TEXT, description TEXT, user_rating INT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

DBC.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, reviews TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

DBC.execute("CREATE TABLE IF NOT EXISTS reviews(game_id INT, body TEXT, user_id INT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

app.secret_key = "secret_key_testing"

@app.route("/")
def main():
    return "P04 Temp Site"


@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == 'POST':
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if not username or not password:
      return render_template('login.html', error="Please enter both username and password")

    db = sqlite3.connect(DB_NAME)
    c = db.cursor()
    c.execute("SELECT username, password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    db.close()

    if not user or user[2] != password:
      text = "Login failed. Invalid username or password."
      return render_template('login.html', error=text)

    session['username'] = username
    return redirect(url_for('homepage'))

  return render_template('login.html', error="")

@app.route("/homepage")
def homepage():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('homepage.html',error="")


@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")
    reviews=""
    if not username or not email or not password or not confirm:
      return render_template("register.html", error="All fields are required!")

    if password != confirm:
      return render_template("register.html", error="Passwords do not match!")



    db = sqlite3.connect(DB_NAME)
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    if c.fetchone():
      db.close()
      return render_template("register.html", error="Username already taken!")

    c.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
    (username, password, reviews, 0))

    db.commit()
    db.close()

    session['username'] = username
    return redirect(url_for("homepage"))

  return render_template("register.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
