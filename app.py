from flask import Flask, jsonify, request
import psycopg2
import requests
import sqlite3

app = Flask(__name__)


def init_db():
    con = psycopg2.connect("dbname=asap user=hdiwan")
    with con.cursor() as cursor:
        cursor.execute(
            """create table if not exists tbl (id text primary key, first_name text, last_name text, dob date, country text)"""
        )
    con.commit()
    con.close()


@app.route("/member_id", methods=["POST"])
def postMemberId():
    with psycopg2.connect("dbname=asap user=hdiwan") as con:
        d = request.json
        with con.cursor() as cursor:
            id_newest = str(
                requests.get("https://units.d8u.us/random?length=16")
                .json()
                .get("integer")
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
    return d


@app.route("/member_id/verify", methods=["GET", "POST"])
def verify():
    con = psycopg2.connect("dbname=asap user=hdiwan")
    query = request.args.get("cc")
    with con.cursor() as con:
        cursor.execute("select id from tbl where id = %s", (query,))
        results = cursor.fetchall()
        return {"exists": results > 0}
    con.close()
