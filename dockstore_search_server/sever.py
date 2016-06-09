import psycopg2
import json

from flask import Flask

app = Flask(__name__)

@app.route("/search_keywords=<name>")
def limhello(name):
    conn_string = "host='localhost' dbname='dockstore' user='ulim' password='3233173'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    pattern = u'%' + name + u'%'
    # SELECT json_object('{key1, 6.4, key2, 9, key3, "value"}');
    cur.execute("SELECT row_to_json(row(name, author, description)) FROM gmod_tools \
                 WHERE LOWER(author) LIKE LOWER(%s)", (pattern,))
    authors = cur.fetchall()

    result_arr = []
    for author_item in authors:
        result_dict = {}
        result_dict["name"] = json.loads(author_item[0])['f1']
        result_dict["author"] = json.loads(author_item[0])['f2']
        result_dict["description"] = json.loads(author_item[0])['f3']
        result_arr.append(result_dict)

    # author_one = json.loads(authors[0][0])['f1']
    cur.close()
    conn.close()
    return json.dumps(result_arr)

if __name__ == "__main__":
    app.run()
