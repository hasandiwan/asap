from flask import Flask, jsonify, request
import psycopg2
import requests
import sqlite3

app = Flask(__name__)


HEROKU_URL = '''"dbname=d9mh10tlos4hmf host=ec2-54-209-52-160.compute-1.amazonaws.com port=5432 user=lkilbjwglsmcin password=159cf3a15b8f979d8b85c00eea0c0f0ee495498782ccdfdefc7b42feb8a5dd07 sslmode=require'''
def init_db():
    try:
        con = psycopg2.connect("dbname=asap user=hdiwan")
    except:
        con = psycopg2.connect(HEROKU_URL)

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
