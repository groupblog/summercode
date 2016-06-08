#import psycopg2
import urllib2
import json

response=urllib2.urlopen('https://www.dockstore.org:8443/api/v1/tools')
html=response.read()
output=open('output','wb')
output.write(html)
output.close()
html=json.loads(html)
print html

conn=psycopg2.connect("dbname=summercode user=yifeiwang")
cur=conn.cursor()

cur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ga4gh/api/v1/tools';")
if not bool(cur.rowcount):
    cur.execute("CREATE TABLE ga4gh/api/v1/tools "
                "(global-id varchar PRIMARY KEY,"
                " registry-id varchar,"
                " registry varchar,"
                " organization varchar,"
                " name varchar,"
                " tooltype jsonb,"
                " description varchar,"
                " author varchar,"
                " meta-version varchar);")
cur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ga4gh/api/v1/tools/versions';")
if not bool(cur.rowcount):
    cur.execute("CREATE TABLE ga4gh/api/v1/tools/versions"
                "(name varchar,"
                "global-id varchar PRIMARY KEY,"
                "toolsGlobal-id varchar,"
                "registry-id varchar,"
                "image varchar,"
                "descriptor jsonb,"
                "dockerfile jsonb,"
                "meta-version varchar);")

set = set()
cur.execute("SELECT global-id FROM ga4gh/api/v1/tools;")
globalIds=cur.fetchall()
for item in globalIds:
   set.add(item)

for item in html:
    if not item["global-id"] in set:
        cur.execute("INSERT INTO ga4gh/api/v1/tools VALUES"
                    "(%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                    (item["global-id"], item["registry-id"], item["registry"],
                     item["organization"], item["name"], json.dumps(item["tooltype"]),
                     item["description"], item["author"], item["meta-version"]))
        for version in item["version"]:
            cur.execute("INSERT INTO ga4gh/api/v1/tools/versions VALUES"
                        "(%s, %s, %s, %s, %s, %s, %s);",
                        (version["name"], version["global-id"], item["global-id"], version["registry-id"],
                         version["image"], json.dumps(version["descriptor"]), json.dumps(version["dockerfile"]),
                         version["meta-version"]))
    else:
        set.remove(item["global-id"])

for id in set:
    cur.execute("DELETE FROM ga4gh/api/v1/tools/versions WHERE toolsGlobal-id = %s;", (item[id],))
    cur.execute("DELETE FROM ga4gh/api/v1/tools WHERE global-id = %s;", (item[id],))


conn.commit()
cur.close()
conn.close()