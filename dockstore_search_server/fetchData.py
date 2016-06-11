import psycopg2
import json
from flask import Flask
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

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
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__)

@app.route('/data/<name>/')
@crossdomain(origin='*', methods='*')
def get_data(name):
	conn=psycopg2.connect("dbname=summercode user=yifeiwang")
	cur=conn.cursor()
	ret=[]
	pattern="'"+name+"%'"
	cur.execute("SELECT * FROM ga4gh_api_v1_tools WHERE name like %s;" % pattern)
	results=cur.fetchall()
	print len(results)
	for row in results:
		entry={}
		# entry["global-id"]=row[0]
		# entry["registry-id"]=row[1]
		# entry["registry"]=row[2]
		# entry["organization"]=row[3]
		entry["name"]=row[4]
		# entry["tooltype"]=row[5]
		# entry["description"]=row[6]
		entry["author"]=row[7]
		# entry["meta-version"]=row[8]
		versions=[]
		Gid="'"+row[0]+"'"
		cur.execute("SELECT * FROM ga4gh_api_v1_tools_versions WHERE name='latest' and toolsGlobalId=%s;" % Gid)
		resultsV=cur.fetchall()[0]
		# entryV={}
		# for rowV in resultsV:
			# entryV["name"]=rowV[0]
			# entryV["global-id"]=rowV[1]
			# entryV["toolsGlobal-id"]=rowV[2]
			# entryV["registry-id"]=rowV[3]
		entry["image"]=resultsV[4]
			# entryV["descriptor"]=rowV[5]
			# entryV["dockerfile"]=rowV[6]
			# entryV["meta-version"]=rowV[7]
			# versions.append(entryV)
		# entry["versions"]=versions
		ret.append(entry)
	conn.commit()
	cur.close()
	conn.close()
	return json.dumps(ret)

if __name__ == '__main__':
	app.run(debug=True)