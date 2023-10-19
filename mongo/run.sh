#!/bin/sh
# Start mongo, run the setup script, follow the log
# --bind_ip 0.0.0.0 --port 27017 --auth --fork --logpath ./mongod.log
# iptables -I INPUT -s 192.168.1.2,127.0.0.1 -p tcp --destination-port 27017 -m state --state NEW,ESTABLISHED -j ACCEPT
# iptables -I OUTPUT -d 192.168.1.2,127.0.0.1 -p tcp --source-port 27017 -m state --state ESTABLISHED -j ACCEPT
# iptables -A INPUT -j DROP
# iptables -A OUTPUT -j DROP
# iptables-save
nohup mongod -f /opt/mongodb/mongod.conf
mongo < ./setupMongo.js 
tail -f ./mongod.log