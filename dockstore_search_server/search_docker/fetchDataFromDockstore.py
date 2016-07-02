import psycopg2
import urllib2
import json

response=urllib2.urlopen('https://www.dockstore.org:8443/api/v1/tools')
html=response.read()
output=open('output','wb')
output.write(html)
output.close()
html=json.loads(html)
# print html

conn=psycopg2.connect("dbname=summercode user=yifeiwang")
cur=conn.cursor()

cur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ga4gh_api_v1_tools';")
if not bool(cur.rowcount):
    cur.execute("CREATE TABLE ga4gh_api_v1_tools "
                "(path varchar PRIMARY KEY,"
                " url varchar,"
                # " registry varchar,"
                " organization varchar,"
                # " name varchar,"
                " name varchar,"
                " tooltype jsonb,"
                " description varchar,"
                " author varchar,"
                " metaVersion varchar,"
                " contains text[]);")
cur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ga4gh_api_v1_tools_versions';")
if not bool(cur.rowcount):
    cur.execute("CREATE TABLE ga4gh_api_v1_tools_versions"
                "(name varchar,"
                "id varchar,"
                "path varchar,"
                "url varchar PRIMARY KEY,"
                "image varchar,"
                "descriptor jsonb,"
                "dockerfile jsonb,"
                "metaVersion varchar);")

set = set()
cur.execute("SELECT path FROM ga4gh_api_v1_tools;")
globalIds=cur.fetchall()
for item in globalIds:
   set.add(item)

for item in html:
    if not item["id"] in set:
        cur.execute("INSERT INTO ga4gh_api_v1_tools VALUES"
                    "(%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                    (item["id"], item["url"],
                     item["organization"], item["toolname"], 
                     json.dumps(item["tooltype"]), item["description"], 
                     item["author"], item["meta-version"], item["contains"]))
        for version in item["versions"]:
            cur.execute("INSERT INTO ga4gh_api_v1_tools_versions VALUES"
                        "(%s, %s, %s, %s, %s, %s, %s, %s);",
                        (version["name"], version["id"], item["id"], version["url"],
                         version["image"], json.dumps(version["descriptor"]), json.dumps(version["dockerfile"]),
                         version["meta-version"]))
    else:
        set.remove(item["id"])

for id in set:
    cur.execute("DELETE FROM ga4gh_api_v1_tools_versions WHERE path = %s;", (id,))
    cur.execute("DELETE FROM ga4gh_api_v1_tools WHERE path = %s;", (id,))


conn.commit()
cur.close()
conn.close()