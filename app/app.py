from flask import Flask, render_template

app = Flask(__name__)
user = "Roberto"


@app.route("/index")
@app.route("/index/<name>")
def index(name=None):
    return render_template("index.html", name=name)
