from app import app, init_db
import psycopg2
import pytest
import simplejson as json
import tempfile
import timeout_decorator


@pytest.fixture
def client():
    app.TESTING = True
    with app.test_client() as client:
        print('in context')
        with app.app_context():
            init_db()
        yield client
    with psycopg2.connect("dbname=asap user=postgres") as con:
        with con.cursor() as cursor:
            cursor.execute(
                "SELECT pid, pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = current_database() AND pid <> pg_backend_pid();drop table if exists tbl"
            )
    con.commit()


@timeout_decorator.timeout(35)
def test_post(client):
    body = {
        "id": 378282246310005,
        "first_name": "Jose",
        "last_name": "Vasconcelos",
        "dob": "01/01/1961",
        "country": "MX",
    }
    rv = client.post("/member_id", json=body)
    body_plus_id = json.loads(rv.data)
    assert "Unexpected output", body == body_plus_id


@timeout_decorator.timeout(5)
def test_get(client):
    rv = client.get("/member_id/validate?id=378282246310005")
    body = rv.json
    assert 'body is invalid', json.loads(body).get("exists")
