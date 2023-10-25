#!/bin/sh
# Start mongo, run the setup script, follow the log
nohup mongod -f /opt/mongodb/mongod.conf
cat <<EOF > ./setupMongo.js
use vision_db;
use admin;
if (!db.auth('$MONGO_ADMIN_USER','$MONGO_ADMIN_PASS')) {
    db.createUser(
        {
            user: '$MONGO_ADMIN_USER',
            pwd: '$MONGO_ADMIN_PASS',
            roles: [
                "userAdminAnyDatabase",
                "dbAdminAnyDatabase",
                "readWriteAnyDatabase"
            ]
        }
    )
}
db.auth('$MONGO_ADMIN_USER', '$MONGO_ADMIN_PASS');
if (!db.auth('$MONGO_USER_USER','$MONGO_USER_PASS')) {
    db.createUser(
        {
            user: '$MONGO_USER_USER',
            pwd: '$MONGO_USER_PASS',
            roles: [
                {
                    role: 'readWrite',
                    db: 'vision_db'
                }
            ]
        }
    )
}
EOF
mongo < ./setupMongo.js 
tail -f ./mongod.log