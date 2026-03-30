from flask import *

app = Flask(__name__)

@app.route("/")
def main():
    return "P04 Temp Site"
    
if __name__ == "__main__":
    app.debug = True
    app.run()