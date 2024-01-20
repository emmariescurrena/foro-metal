import os
import psycopg2
from flask import *

app = Flask(__name__)

with open('sql.txt', 'r') as file:
    sqlArr = file.read().splitlines()


def titulo_a_url(titulo):
    url = ""
    titulo = titulo.rstrip()
    titulo = titulo.lstrip()
    for char in titulo:
        if char in "aeiouáéíóúbcdfghjklmnñpqrstvwxyz":
            url += char
        elif char in "AEIOUÁÉÍÓÚBCDFGHJKLMNÑPQRSTVWXYZ":
            url += char.lower()
        elif char == " " and url[-1] != "-":
            url += "-"
    return url


def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='foro_de_metal',
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )
    return conn


@app.route("/")
def root():
    return redirect(url_for('index'))


@app.route("/index")
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    sql = sqlArr[0]
    cur.execute(sql)
    topicos = cur.fetchall()

    cur.close()
    conn.close()
    return render_template("index.html", topicos=topicos)


@app.route("/<url>")
def topico(url=None):
    conn = get_db_connection()
    cur = conn.cursor()

    sql = f"{sqlArr[1]} '{url}';"
    cur.execute(sql)
    topico = cur.fetchone()
    id_topico = topico[5]

    sql = f"{sqlArr[2]} '{id_topico}';"
    cur.execute(sql)
    respuestas = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("topico.html", topico=topico, respuestas=respuestas)


@app.route("/<nombreUsuario>")
def usuario(nombreUsuario=None):
    conn = get_db_connection()
    cur = conn.cursor()

    sql = f"{sqlArr[3]} '{nombreUsuario}';"
    cur.execute(sql)
    usuario = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("usuario.html", usuario=usuario)


if __name__ == '__main__':
    app.run(debug=True)
