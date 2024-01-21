"""Import os to access environ to export DB username and password"""
import os
import psycopg2
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

with open('sql.txt', 'r', encoding="UTF-8") as file:
    sql_arr = file.read().splitlines()


def titulo_a_url(titulo):
    """Simplifica titulo del tópico para poder ser guardado como url"""
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
    """Get connection to 'foro_de_metal' database"""
    conn = psycopg2.connect(
        host='localhost',
        database='foro_de_metal',
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )
    return conn


@app.route("/")
def root():
    """Redirects from root to index"""
    return redirect(url_for('index'))


@app.route("/topicos")
def index():
    """Connects to DB and render template for index"""
    conn = get_db_connection()
    cur = conn.cursor()

    sql = sql_arr[0]
    cur.execute(sql)
    topicos = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", topicos=topicos)


@app.route("/topicos/<url>")
def topico(url=None):
    """Connects to DB and render template for topico"""
    conn = get_db_connection()
    cur = conn.cursor()

    sql = f"{sql_arr[1]} '{url}';"
    cur.execute(sql)
    info_topico = cur.fetchone()
    id_topico = info_topico[5]

    sql = f"{sql_arr[2]} '{id_topico}';"
    cur.execute(sql)
    respuestas = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("topico.html", info_topico=info_topico, respuestas=respuestas)


@app.route("/usuario/<nombre_usuario>")
def usuario(nombre_usuario=None):
    """Connects to DB and render template for usuario"""
    conn = get_db_connection()
    cur = conn.cursor()

    sql = f"{sql_arr[3]} '{nombre_usuario}';"
    cur.execute(sql)
    info_usuario = cur.fetchone()
    print(info_usuario)

    cur.close()
    conn.close()

    return render_template("usuario.html", info_usuario=info_usuario)


if __name__ == '__main__':
    app.run(debug=True)
