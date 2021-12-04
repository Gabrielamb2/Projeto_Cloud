#!/bin/bash
cd /
sudo apt update && sudo apt install postgresql postgresql-contrib -y
sudo -u postgres psql -c "CREATE ROLE cloud WITH PASSWORD '%s';"
sudo -u postgres psql -c "ALTER ROLE cloud WITH PASSWORD '%s';"
sudo -u postgres psql -c "ALTER USER cloud WITH LOGIN;"
sudo -u postgres psql -c "create database tasks;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE tasks TO cloud;"
sudo -u postgres psql -c "CREATE TABLE [IF NOT EXISTS] tasks (title VARCHAR(50), pub_date TIMESTAMP, description VARCHAR(500));"
echo "listen_addresses = '*'" >>  /etc/postgresql/10/main/postgresql.conf
echo "host all all 0.0.0.0/0 trust" >> /etc/postgresql/10/main/pg_hba.conf
EOF
sudo ufw allow 5432/tcp
sudo systemctl restart postgresql