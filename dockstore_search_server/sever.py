import psycopg2
from flask import Flask

app = Flask(__name__)

@app.route("/search_keywords=<name>")
def limhello(name):
    conn_string = "host='localhost' dbname='dockstore' user='ulim' password='3233173'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute("SELECT author, name FROM gmod_tools;")
    authors = cur.fetchall()
    cur.close()
    conn.close()
    return str(authors)

if __name__ == "__main__":
    app.run()
