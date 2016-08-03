import psycopg2
import json

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

from flask import Flask

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__)

@app.route("/search_keywords=<name>")
@crossdomain(origin='*')
def limhello(name):
    conn_string = "host='localhost' dbname='dockstore' user='ulim' password='3233173'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    pattern = u'%' + name + u'%'
    # SELECT json_object('{key1, 6.4, key2, 9, key3, "value"}');
    cur.execute("SELECT row_to_json(row(name, author, description, globalId)) FROM gmod_tools \
                 WHERE LOWER(author) LIKE LOWER(%s) OR LOWER(name) LIKE LOWER(%s);", (pattern, pattern))
    authors = cur.fetchall()

    master_version = json.loads(authors[0][0])['f4'] + "/version/latest"

    cur.execute("SELECT image from gmod_tools_versions_table \
                 WHERE globalId = %s;", (master_version,))

    image_url = cur.fetchall()[0][0]

    result_arr = []
    for author_item in authors:
        result_dict = {}
        result_dict["name"] = json.loads(author_item[0])['f1']
        result_dict["author"] = json.loads(author_item[0])['f2']
        result_dict["image"] = image_url
        result_arr.append(result_dict)

    # author_one = json.loads(authors[0][0])['f1']
    cur.close()
    conn.close()
    return json.dumps(result_arr)

if __name__ == "__main__":
    app.run()
