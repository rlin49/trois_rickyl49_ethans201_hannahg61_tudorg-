from flask import *
import os, json, sqlite3, random

app = Flask(__name__)

app.secret_key = "wierhaweuhr890235hj    aeb;sdfb'a34-2q[PAF]"

DB_NAME = "Data/database.db"
DB = sqlite3.connect(DB_NAME)
DBC = DB.cursor()

DBC.execute("CREATE TABLE IF NOT EXISTS games(name TEXT, reviews TEXT, user_rating INT, num_ratings INT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

DBC.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, reviews TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

DBC.execute("CREATE TABLE IF NOT EXISTS reviews(game_id INT, body TEXT, user_id INT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

app.secret_key = "secret_key_testing"

@app.route("/")
def main():
    return redirect(url_for("login"))




@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/homepage")
def homepage():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        username='username'
        return render_template('homepage.html',username=username, error="")


@app.route("/game", methods = ["GET", "POST"])
def game():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        json_file = open("Data/games.json", "r")
        data = json.load(json_file)
        data_keys = list(data.keys())
        guessed_amt = ""
        real_amt = ""
        game_arr = ""

        if "game_index" in request.form:
            check_name = data_keys[int(request.form["game_index"])]
            check_dict = data[check_name]

            game_arr = request.form["game_arr"].split(";")
            guessed_amt = request.form["guess_arr"].split(";")
            real_amt = request.form["ans_arr"].split(";")

            game_arr.append(str(int(request.form["game_index"])))
            guessed_amt.append(str(round(float(request.form["guessed_sales"]), 4)))
            real_amt.append(str(round(float(check_dict["Global_Sales"]), 4)))


            guessed_amt = ";".join(guessed_amt)
            real_amt = ";".join(real_amt)
            game_arr = ";".join(game_arr)

            if guessed_amt[0] == ";":
                guessed_amt = guessed_amt[1:]
            if real_amt[0] == ";":
                real_amt = real_amt[1:]
            if game_arr[0] == ";":
                game_arr = game_arr[1:]



        game_index = random.randint(0, len(data_keys))
        game_name = data_keys[game_index]
        info_dict = data[game_name]


        sales_rank = info_dict["Rank"]
        platforms = info_dict["Platform"]
        year = info_dict["Year"]
        genre = info_dict["Genre"]
        publisher = info_dict["Publisher"]
        public_rating = info_dict["public_rating"]
        if public_rating == -1:
            public_rating = "No Metacritic Score was Available"
        description = info_dict["description"]

        return render_template('game.html', guess_arr = guessed_amt, ans_arr = real_amt, game_arr = game_arr, game_name = game_name, game_index = game_index, rank = sales_rank, platform = platforms, year = year, genre = genre, publisher = publisher, rating = public_rating, description = description)

@app.route("/profile/<username>")
def profile(username):
    if 'username' not in session:
        return redirect(url_for('login'))
    user=session['username']
    print(user)
    if username != session['username']:
        is_own_profile=False
    else:
        is_own_profile=True
    print(is_own_profile)
    return render_template("profile.html",username=user, is_own_profile=is_own_profile)

# THESE ARE HERE TO MAKE SURE /LOGIN.HTML AND /REGISTER.HTML WORK. DO NOT REMOVE
@app.route("/login.html")
def loginhtml():
    if 'username' in session:
        return redirect("/")
    return render_template("login.html")

@app.route("/register.html")
def registerhtml():
    if 'username' in session:
        return redirect("/")
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
  if 'username' in session:
      return redirect(url_for('homepage'))
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

    if not user or user[1] != password:
      text = "Login failed. Invalid username or password."
      return render_template('login.html', error=text)

    session['username'] = username
    return redirect(url_for('homepage'))

  return render_template('login.html', error="")


@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    username = request.form.get("username", "").strip()
    # email = request.form.get("email", "").strip() why would we need an email
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")
    reviews=""
    if not username or not password or not confirm:
      return render_template("register.html", error="All fields are required!")

    if password != confirm:
      return render_template("register.html", error="Passwords do not match!")

    db = sqlite3.connect(DB_NAME)
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    if c.fetchone():
      db.close()
      return render_template("register.html", error="Username already taken!")

    c.execute("INSERT INTO users (username, password, reviews) VALUES (?, ?, ?)",
    (username, password, reviews))

    db.commit()
    db.close()

    session['username'] = username
    return redirect(url_for("homepage"))

  return render_template("register.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
