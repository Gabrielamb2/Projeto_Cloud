#!/bin/bash
cd home/ubuntu/
sudo apt update -y
git clone https://github.com/raulikeda/tasks.git
cd tasks
sed -i 's/node1/postgres_ip/g' ./portfolio/settings.py
./install.sh
sudo ufw allow 8080/tcp -y
sudo reboot