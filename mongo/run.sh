#!/bin/sh
# Start mongo, run the setup script, follow the log
nohup mongod --bind_ip 0.0.0.0 --port 27017 --auth --fork --logpath ./mongod.log && mongo < ./setupMongo.js && tail -f ./mongod.log