import urllib
import json
import psycopg2


conn = psycopg2.connect("dbname='mydb' user='postgres' password='123' host='localhost'")
print "Opened database successfully"

cur = conn.cursor()

cur.execute("SELECT * FROM information_schema.tables WHERE table_name='tools';")
if not bool(cur.rowcount):
	cur.execute("CREATE TABLE tools (globalID	varchar	PRIMARY KEY, registryID	varchar, registry	varchar, organization	varchar, name	varchar, toolname	varchar, tooltype	json, description	varchar, author	varchar, metaVersion	varchar );")

cur.execute("SELECT * FROM information_schema.tables WHERE table_name='tools_versions';")
if not bool(cur.rowcount):       
	cur.execute("CREATE TABLE tools_versions (name	varchar, globalID	varchar primary key, registryID	varchar, image	varchar, descriptor	json, dockerfile	json, metaVersion	varchar);")


tools_ord_list = []
cur.execute("SELECT globalID FROM tools")
tools_ord_ids = cur.fetchall()
for i in tools_ord_ids:
	tools_ord_list.append(i)

tools_versions_ord_list = []
cur.execute("SELECT globalID FROM tools_versions")
tools_versions_ord_ids = cur.fetchall()
for j in tools_versions_ord_ids:
	tools_versions_ord_list.append(j)

f = urllib.urlopen("new.json")
nf = json.loads(f.read())

tools_new_list = []
tools_versions_new_list = []
for i in nf:
	tools_new_list.append(i["global-id"])
	for j in i["versions"]:
		tools_versions_new_list.append(j["global-id"])

add_tools_list = list(set(tools_new_list) - set(tools_ord_list))
remove_tools_list = list(set(tools_ord_list) - set(tools_new_list))

add_tools_versions_list = list(set(tools_versions_new_list) - set(tools_versions_ord_list))
remove_tools_version_list = list(set(tools_versions_ord_list) - set(tools_versions_new_list))

for item in remove_tools_list:
	cur.execute("DELETE FROM tools WHERE globalID = %s;", (item))

for item in remove_tools_version_list:
	cur.execute("DELETE FROM tools_versions WHERE globalID = %s;", (item))

for item in nf:
	if item["global-id"] in add_tools_list:
		cur.execute("INSERT INTO tools (globalID, registryID, registry, organization, name, toolname, tooltype, description, author, metaVersion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (item["global-id"], item["registry-id"], item["registry"], item["organization"], item["name"], item["toolname"], json.dumps(item["tooltype"]), item["description"], item["author"], item["meta-version"]))
		for version in item["versions"]:
			if version["global-id"] in add_tools_versions_list:
				cur.execute("INSERT INTO tools_versions (name, globalID, registryID, image, descriptor, dockerfile, metaVersion) VALUES (%s, %s, %s, %s, %s, %s, %s);", (version["name"], version["global-id"], version["registry-id"], version["image"], json.dumps(version["descriptor"]), json.dumps(version["dockerfile"]), version["meta-version"]))

conn.commit()

conn.close() 
