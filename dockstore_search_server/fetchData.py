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
	# print len(results)
	for row in results:
		entry={}
		entry["path"]=row[0]
		# entry["url"]=row[1]
		# entry["organization"]=row[2]
		entry["name"]=row[3]
		# entry["tooltype"]=row[4]
		# entry["description"]=row[5]
		entry["author"]=row[6]
		# entry["metaVersion"]=row[7]
		# entry["contains"]=row[8]
		# versions=[]
		# Gid="'"+row[0]+"'"
		# cur.execute("SELECT * FROM ga4gh_api_v1_tools_versions WHERE path=%s;" % Gid)
		# resultsV=cur.fetchall()
		# for rowV in resultsV:
		# 	entryV={}
		# 	entryV["name"]=rowV[0]
		# 	entryV["id"]=rowV[1]
		# 	entryV["path"]=rowV[2]
		# 	entryV["url"]=rowV[3]
		# 	entryV["image"]=rowV[4]
		# 	entryV["descriptor"]=rowV[5]
		# 	entryV["dockerfile"]=rowV[6]
		# 	entryV["meta-version"]=rowV[7]
		# 	versions.append(entryV)
		# entry["versions"]=versions
		entry["gitUrl"]="https://github.com/ga4gh"
		entry["toolname"]=""
		ret.append(entry)
	conn.commit()
	cur.close()
	conn.close()
	return json.dumps(ret)

if __name__ == '__main__':
	app.run(debug=True)