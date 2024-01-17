import os
import psycopg2
from flask import *
import json

app = Flask(__name__)


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
@app.route("/index")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT url, nombre FROM topicos;")
    topicos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", topicos=topicos)


@app.route("/<url>")
def topico(url=None):
    conn = get_db_connection()
    cur = conn.cursor()

    def get_topico_and_usuario(url):
        with open('sql/get_topico_and_usuario.txt', 'r') as file:
            sql = f"{file.read()} '{url}';"
        cur.execute(sql)
        topico = cur.fetchone()
        return topico
    topico = get_topico_and_usuario(url)
    id_topico = topico[5]

    def get_respuestas_with_usuarios(id_topico):
        with open('sql/get_respuestas_with_usuarios.txt', 'r') as file:
            sql = f"{file.read()} '{id_topico}';"
        cur.execute(sql)
        respuestas = cur.fetchall()
        return respuestas
    respuestas = get_respuestas_with_usuarios(id_topico)

    cur.close()
    conn.close()

    return render_template("topico.html", topico=topico, respuestas=respuestas)
