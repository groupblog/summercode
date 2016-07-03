### Usage

- Postgres database configuration should be done in run.sh, createTable.py and fetchData.py
- To build a search server:
```
$ sudo docker build -t search-server .
```
- To run a search server:
```
$ sudo docker run [-d] -p 5000:5000 search-server
```