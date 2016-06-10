import psycopg2
import json
from flask import Flask
app = Flask(__name__)

@app.route('/data/<name>/')
def get_data(name):
	conn=psycopg2.connect("dbname=summercode user=yifeiwang")
	cur=conn.cursor()
	ret=[]
	pattern="'"+name+"%'"
	cur.execute("SELECT * FROM ga4gh_api_v1_tools WHERE name like %s;" % pattern)
	results=cur.fetchall()
	entry={}
	for row in results:
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