from flask import *
import os, json, sqlite3, random, urllib
import games, users, reviews

app = Flask(__name__)

app.secret_key = "wierhaweuhr890235hj    aeb;sdfb'a34-2q[PAF]"

DB_NAME = "Data/database.db"
DB = sqlite3.connect(DB_NAME)
DBC = DB.cursor()

DBC.execute("CREATE TABLE IF NOT EXISTS games(name TEXT, reviews TEXT, user_rating INT, num_ratings INT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

DBC.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT,bio TEXT, reviews TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

DBC.execute("CREATE TABLE IF NOT EXISTS reviews(game_id INT, body TEXT, user_id INT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

app.secret_key = "secret_key_testing"

@app.route("/")
def main():
    return redirect(url_for("homepage"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("homepage"))

@app.route("/homepage")
def homepage():
    if 'username' not in session:
        username = "Guest"
        logged_in = False
    else:
        username = session['username']
        logged_in = True

    db = sqlite3.connect(DB_NAME)
    c = db.cursor()
    c.execute("SELECT name FROM games ORDER BY user_rating DESC LIMIT 10;")
    fetch = c.fetchall();
    game_ranking = "";
    for game in fetch:
        rating = games.get_rating(game[0])
        if rating != -1:
            game_ranking += f'<a href = "/gamepage/{games.get_id(game[0])}" class="text-blue-700">{game[0]}</a> - {rating}'
            game_ranking += "<br>"

    db = sqlite3.connect(DB_NAME)
    c = db.cursor()
    c.execute("SELECT name FROM games WHERE NOT user_rating = -1 ORDER BY user_rating ASC LIMIT 10;")
    fetch = c.fetchall();
    bad_ranking = "";
    for game in fetch:
        rating = games.get_rating(game[0])
        print(rating)
        if rating != -1:
            bad_ranking += f'<a href = "/gamepage/{games.get_id(game[0])}" class="text-blue-700">{game[0]}</a> - {rating}'
            bad_ranking += "<br>"

    c.execute("SELECT user_rating FROM games ORDER BY user_rating;")
    fetch = c.fetchall();

    full_ratings = []
    for rate in fetch:

        if rate[0] is not None and rate[0] != -1:
            full_ratings.append(str(rate[0]))

    full_ratings = ";".join(full_ratings)


    return render_template('homepage.html',username= username, error="", game_ranking = game_ranking, bad_ranking = bad_ranking, logged_in = logged_in, full_ratings = full_ratings)

@app.route("/screwuptheratingsletsago")
def screwitup():
    if 'username' not in session or session['username'] != "test":
        return redirect(url_for('homepage'))
    else:
        for i in range(0,10):
            for i in range(0,1000):
                integer_fun = random.randint(0,100)
                games.add_rating(integer_fun, i)
        return redirect(url_for('homepage'))

@app.route("/gamepage/<game_id>", methods = ["GET", "POST"])
def gamepage(game_id):
    if 'username' not in session:
        username = "Guest"
        logged_in = False
    else:
        username = session['username']
        logged_in = True
    # if 'username' not in session:
    #     return redirect(url_for('login'))
    # if "game_id" not in request.args:
    #     return redirect(url_for('search'))
    if 'username' not in session:
        logged_in = False
    else:
        username = session['username']
        logged_in = True
    json_file = open("Data/games.json", "r")
    data = json.load(json_file)
    data_keys = list(data.keys())

    game_id = int(game_id)
    # game_id = int(request.args["game_id"])
    if game_id < 0 or game_id >= len(data_keys):
        return redirect(url_for("homepage"))


    game_name = data_keys[game_id]
    info_dict = data[game_name]


    user_ranking = games.get_rating(game_id)
    if not isinstance(user_ranking, int) or games.get_num_ratings(game_id) == 0:
        user_ranking = "No data yet"

    rank = info_dict["Rank"]
    platforms = info_dict["Platform"]
    year = info_dict["Year"]
    genre = info_dict["Genre"]
    publisher = info_dict["Publisher"]
    na_sales = info_dict["NA_Sales"]
    eu_sales = info_dict["EU_Sales"]
    jp_sales = info_dict["JP_Sales"]
    other_sales = info_dict["Other_Sales"]
    global_sales = info_dict["Global_Sales"]
    rating = info_dict["public_rating"]
    if rating == -1:
        rating = "No Metacritic Score was Available"
    description = info_dict["description"]
    description = description.replace("<br />", "")
    description = description.replace("<p>", "")
    description = description.replace("</p>", "")

    db = sqlite3.connect(DB_NAME)
    c = db.cursor()

    file = open("keys/key_rawg.txt")
    api_key = file.read().strip()
    base_link = "https://api.rawg.io/api/games/"
    addition = f"/screenshots?key={api_key}"

    bad_chars = [":", "/", "!", "'", "&", "(", ")"]
    parentheticalizing = False

    try:
        temp = ""
        for i in game_name:
            if i == " ":
                temp += "-"
            elif i not in bad_chars:
                temp += i
            elif i == "&":
                temp += "and"
        print(temp)
        img_link = base_link + temp + addition
        print(img_link)
        img_req = urllib.request.urlopen(img_link)
        img_json = img_req.read()
        img_data = json.loads(img_json)
        print(img_data)
        if "detail" in img_data:
            img_link = ""
        if "results" in img_data:
            img_link = img_data["results"][0]["image"]
    except:
        print("huh")
        img_link = ""

    review_arr= games.get_reviews(game_id).split(";")
    review_str = ""

    for i in range(len(review_arr)):
        if len(review_arr) == 1 and review_arr[0] == "":
            break
        review_str += reviews.get_review(review_arr[i])
        user = users.get_username(reviews.get_user(review_arr[i]))
        if user is None:
            user="Anonymous"
        review_str += " - " + str(user)
        review_str += "<br>"

#    for rev in review_arr:
#        review_str += reviews.get_review(rev)
#        review_str += "<br>"

    return render_template("gamepage.html", username = username, logged_in = logged_in, img_link = img_link, game_id = game_id, game_name = game_name, user_ranking = user_ranking, reviews = review_str,  rank = rank, platforms = platforms, year = year, genre = genre, publisher = publisher, na_sales = na_sales, eu_sales = eu_sales, jp_sales = jp_sales, other_sales = other_sales, global_sales = global_sales, rating = rating, description = description)

@app.route("/purgeall")
def purgeall():
    if 'username' not in session or session['username'] != "test":
        return redirect(url_for("homepage"))
    for i in range(0,1000):
        games.purge_reviews(i)
        games.purge_ratings(i)
    return redirect(url_for("homepage"))

@app.route("/purge", methods = ["GET", "POST"])
def purge():
    if 'username' not in session or session['username'] != "test":
        return redirect(f"/gamepage/{request.form['game_id']}")
    if 'game_id' not in request.form:
        return redirect(url_for('search'))

    game_id = int(request.form["game_id"])
    games.purge_reviews(game_id)
    games.purge_ratings(game_id)

    return redirect(f"/gamepage/{request.form['game_id']}")

@app.route("/rate", methods = ["GET", "POST"])
def rate():
    if 'username' not in session:
        return redirect(url_for('login'))
    if 'game_id' not in request.form or 'rating' not in request.form:
        return redirect(url_for('search'))
    if 'rated_games' not in session:
        session['rated_games']=[]
    game=int(request.form['game_id'])
    if game not in session['rated_games']:
        session['rated_games'].append(game)
        games.add_rating(int(request.form['rating']), int(request.form["game_id"]))
    else:
        flash("You have already rated this game.", "error")
    return redirect(f"/gamepage/{request.form['game_id']}")

@app.route("/review", methods = ["GET", "POST"])
def review():
    if 'username' not in session:
        return redirect(f"/gamepage/{request.form['game_id']}")
    if 'game_id' not in request.form or 'body_text' not in request.form:
        return redirect(url_for('search'))

    game_id = int(request.form["game_id"])
    body_text = request.form["body_text"]
    temp = ""

    for i in body_text:
        if i != ">" and i != "<":
            temp += i

    body_text = temp
    user_id = int(users.get_id(session["username"]))

    reviews.make_review(body_text, user_id, game_id)
    return redirect(f"/gamepage/{game_id}")

@app.route("/search", methods = ["GET", "POST"])
def search():
    if 'username' not in session:
        username = "Guest"
        logged_in = False
    else:
        username = session['username']
        logged_in = True
    # if 'username' not in session:
    #     return redirect(url_for('homepage'))
    if 'username' not in session:
        logged_in = False
    else:
        username = session['username']
        logged_in = True
    if "game_name" in request.args:
        db = sqlite3.connect(DB_NAME)
        c = db.cursor()
        c.execute("SELECT * FROM games WHERE name LIKE '%' || ? || '%';", (request.args["game_name"], ))
        fetch = c.fetchall()

        game_arr = ""
        for game in fetch:
            game_arr += f"<a href = '/gamepage/{game[4] - 1}'>{game[0]}</a><br>"
        return render_template("search.html", username = username, logged_in = logged_in, games = game_arr)
    else:
        return render_template("search.html", username = username, logged_in = logged_in, searching = True)

@app.route("/game", methods = ["GET", "POST"])
def game():

    # if 'username' not in session:
    #     return redirect(url_for('login'))
    # else:
        if 'username' not in session:
            username = "Guest"
            logged_in = False
        else:
            username = session['username']
            logged_in = True

        json_file = open("Data/games.json", "r")
        data = json.load(json_file)
        data_keys = list(data.keys())
        guessed_amt = ""
        real_amt = ""
        game_arr = ""

        if "game_index" in request.form:
            check_name = data_keys[int(request.form["game_index"])]
            check_dict = data[check_name]

            #print(request.form["game_arr"])
            game_arr = request.form["game_arr"].split(";")
            guessed_amt = request.form["guess_arr"].split(";")
            real_amt = request.form["ans_arr"].split(";")


            game_arr.append(data_keys[int(request.form["game_index"])])
            guessed_amt.append(str(round(float(request.form["guessed_sales"]), 4)))
            real_amt.append(str(round(float(check_dict["Global_Sales"]), 4)))
            #print(game_arr)

            guessed_amt = ";".join(guessed_amt)
            real_amt = ";".join(real_amt)
            game_arr = ";".join(game_arr)
            # print(game_arr)

            if guessed_amt[0] == ";":
                guessed_amt = guessed_amt[1:]
            if real_amt[0] == ";":
                real_amt = real_amt[1:]
            if game_arr[0] == ";":
                game_arr = game_arr[1:]




        game_index = random.randint(0, len(data_keys))
        # game_index = random.randint(0,100)
        game_name = data_keys[game_index]
        info_dict = data[game_name]
        img_link = ""
        # file = open("keys/key_rawg.txt")
        # api_key = file.read().strip()
        # base_link = "https://api.rawg.io/api/games/"
        # addition = f"/screenshots?key={api_key}"
        #
        # bad_chars = [":", "/", "!", "'", "&", "(", ")"]
        # parentheticalizing = False
        #
        # try:
        #     temp = ""
        #     for i in game_name:
        #         if i == " ":
        #             temp += "-"
        #         elif i not in bad_chars:
        #             temp += i
        #         elif i == "&":
        #             temp += "and"
        #     print(temp)
        #     img_link = base_link + temp + addition
        #     print(img_link)
        #     img_req = urllib.request.urlopen(img_link)
        #     img_json = img_req.read()
        #     img_data = json.loads(img_json)
        #     print(img_data)
        #     if "detail" in img_data:
        #         img_link = ""
        #     if "results" in img_data:
        #         img_link = img_data["results"][0]["image"]
        # except:
        #     print("huh")
        #     img_link = ""



        sales_rank = info_dict["Rank"]
        platforms = info_dict["Platform"]
        year = info_dict["Year"]
        genre = info_dict["Genre"]
        publisher = info_dict["Publisher"]
        public_rating = info_dict["public_rating"]
        if public_rating == -1:
            public_rating = "No Metacritic Score was Available"
        description = info_dict["description"]
        description = description.replace("<br />", "")
        description = description.replace("<p>", "")
        description = description.replace("</p>", "")

        print("huh")
        return render_template('game.html',username = username, logged_in = logged_in, guess_arr = guessed_amt, ans_arr = real_amt, game_arr = game_arr, game_name = game_name, game_index = game_index, rank = sales_rank, platform = platforms, year = year, genre = genre, publisher = publisher, rating = public_rating, description = description, img_link = img_link)

@app.route("/profile/<username>")
def profile(username):
    if 'username' not in session:
        return redirect(url_for('login'))
    user = session['username']
    is_own_profile = (username == session['username'])

    db = sqlite3.connect(DB_NAME)
    c = db.cursor()
    c.execute("SELECT bio FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    db.close()
    bio = row[0] if row and row[0] else ""

    return render_template("profile.html", username=user, is_own_profile=is_own_profile, bio=bio)

@app.route("/profile")
@app.route("/profile/")
def profilez():
    if 'username' not in session:
        return redirect(url_for('login'))
    return(redirect(url_for("profile", username=session['username'])))
    
@app.route("/update_bio", methods=["POST"])
def update_bio():
    if 'username' not in session:
        return redirect(url_for('login'))
    bio = request.form.get("bio", "").strip()
    db = sqlite3.connect(DB_NAME)
    c = db.cursor()
    c.execute("UPDATE users SET bio = ? WHERE username = ?", (bio, session['username']))
    db.commit()
    db.close()
    return redirect(url_for('profile', username=session['username']))

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

    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, NULL)",
    (username, password,"Bio to be created here!", reviews))

    db.commit()
    db.close()

    session['username'] = username
    if 'rated_games' not in session:
        session['rated_games']=[]
    session.permanent=True
    return redirect(url_for("homepage"))

  return render_template("register.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
