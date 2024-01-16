from flask import *

app = Flask(__name__)


@app.route("/")
def index(name="Roberto"):
    return render_template("index.html", name=name)


@app.route("/topico")
def topico():
    return render_template("topico.html")


usuario = {
    "nombre": "david_musteink",
    "fecha_creacion": "05/06/1998"
}


@app.route("/usuario")
def usuario(usuario=None):
    return render_template("usuario.html", usuario=usuario)
