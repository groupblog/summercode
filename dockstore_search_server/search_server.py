import psycopg2, json
from flask import Flask
app = Flask(__name__)

@app.route('/search/<key>', methods=['GET'])
def search(key):
	patten = '%'+key+'%'
	result_list = []
	db_info = "dbname='mydb' user='postgres' password='12345' host='localhost'"
	conn = psycopg2.connect(db_info)
	cur = conn.cursor()
	cur.execute("SELECT * FROM tools WHERE name LIKE %s OR author LIKE %s;",(patten, patten))
	result_list = cur.fetchall()
	return json.dumps(result_list)

if __name__ == '__main__':
	app.run()
