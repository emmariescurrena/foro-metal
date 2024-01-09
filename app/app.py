from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def index(name="Roberto"):
    return render_template("index.html", name=name)


@app.route("/temas")
def tema():
    return render_template("tema.html")
