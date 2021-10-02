from flask import Flask, jsonify, request
import os
import psycopg2
import requests
import urllib.parse as urlparse

app = Flask(__name__)


HEROKU_URL = os.environ["DATABASE_URL"]


def init_db():
    try:
        con = psycopg2.connect("dbname=asap user=hdiwan")
    except:
        url = urlparse.urlparse(HEROKU_URL)
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        con = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )

    with con.cursor() as cursor:
        cursor.execute(
            """create table if not exists tbl (id text primary key, first_name text, last_name text, dob date, country text)"""
        )
    con.commit()
    con.close()


@app.route("/member_id", methods=["POST"])
def postMemberId():
    try:
        con = psycopg2.connect("dbname=asap user=hdiwan")
    except:
        con = psycopg2.connect(HEROKU_URL)
    d = request.json
    with con.cursor() as cursor:
        id_newest = str(
            requests.get("https://units.d8u.us/random?length=16").json().get("integer")
        ).replace("-", "")
        while True:
            cursor.execute("select id from tbl where id = %s", (id_newest,))
            if cursor.rowcount == 0:
                break
        cursor.execute(
            """INSERT INTO tbl(id, first_name, last_name, dob, country) values(%s,%s,%s,%s,%s)""",
            (
                id_newest,
                d.get("first_name"),
                d.get("last_name"),
                d.get("dob"),
                d.get("country"),
            ),
        )
    con.commit()
    con.close()
    return d


@app.route("/member_id/verify", methods=["GET", "POST"])
def verify():
    try:
        con = psycopg2.connect("dbname=asap user=hdiwan")
    except:
        con = psycopg2.connect(HEROKU_URL)
    query = request.args.get("cc")
    with con.cursor() as con:
        cursor.execute("select id from tbl where id = %s", (query,))
        results = cursor.fetchall()
        return {"exists": results > 0}
    con.close()
