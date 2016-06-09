import psycopg2, json
from flask import Flask
app = Flask(__name__)

@app.route('/search/<key>', methods=['GET'])
def search(key):
	patten = '%' + key + '%'
	result_list = []
	db_info = "dbname='mydb' user='postgres' password='12345' host='localhost'"
	conn = psycopg2.connect(db_info)
	cur = conn.cursor()
	cur.execute("SELECT name, author, registryid FROM tools WHERE name LIKE %s OR author LIKE %s;",(patten, patten))
	result_list = cur.fetchall()
	lists = []
	for item in result_list:
		dirc = {} 
		dirc['name'] = item[0]
		dirc['author'] = item[1]
		dirc['docker pull'] = item[2]
		lists.append(dirc)
	return json.dumps(lists)

if __name__ == '__main__':
	app.run()
