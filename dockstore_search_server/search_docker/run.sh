echo "Starting Postgres"
bash /docker-entrypoint.sh postgres &
sleep 10

# todo put the web service startup here
# echo "Starting Java Web Service"
psql -c "create user yifeiwang with password '966278' createdb;" -U postgres
psql -c "ALTER USER yifeiwang WITH superuser;" -U postgres                                                                                                      
psql -c 'create database summercode owner yifeiwang;' -U postgres 

python createTable.py
python fetchData.py