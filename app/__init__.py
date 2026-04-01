from flask import *
import os, json, sqlite3

app = Flask(__name__)

app.secret_key = "wierhaweuhr890235hj    aeb;sdfb'a34-2q[PAF]"

DB_NAME = "Data/database.db"
DB = sqlite3.connect(DB_NAME)
DBC = DB.cursor()

DBC.execute("CREATE TABLE IF NOT EXISTS games(name TEXT, reviews TEXT, user_rating INT, num_ratings INT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

DBC.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, reviews TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

DBC.execute("CREATE TABLE IF NOT EXISTS reviews(game_id INT, body TEXT, user_id INT, id INTEGER PRIMARY KEY AUTOINCREMENT);")

@app.route("/")
def main():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
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
    if 'username' in session:
      return redirect(url_for('homepage'))  
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            return render_template("register.html", error = True, error_msg = "Please enter both username and password")
            
        db = sqlite3.connect(DB_NAME)
        c = db.cursor()
        c.execute("SELECT COUNT(*) FROM users WHERE username = ?;", (username,))
        alreadyExists = c.fetchone()[0]
        
        if(alreadyExists != 0):
            return render_template("register.html", error = True, error_msg = "Username already taken")
            
        c.execute("INSERT INTO users VALUES(?,?, NULL, NULL);",(username, password,))
        db.commit()
        db.close()
        session['username'] = username
        return redirect(url_for('homepage'))
  
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))       
        
@app.route("/homepage")
def homepage():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('homepage.html',error="")
        
        
    
            
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

if __name__ == "__main__":
    app.debug = True
    app.run()
