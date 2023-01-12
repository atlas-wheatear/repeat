import psycopg2
from flask import Flask, request


app = Flask(__name__)


def password_is_right(password: str) -> bool:
    conn = psycopg2.connect(
        database="postgres",
        user='postgres',
        password='postgres',
        host='db',
        port='5432'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    sql = f"SELECT * FROM users WHERE password = '{password}';"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return len(results) == 1


@app.route('/', methods=['POST'])
def vuln_sql():
    password = request.json.get('password', '')
    if password_is_right(password):
        return 'SUCCESS', 200
    else:
        return 'FAILURE', 403
    