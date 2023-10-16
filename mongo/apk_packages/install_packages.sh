#!/bin/sh
# Install the mongodb and mongo-tools apk packages using the local .apk files
for i in $(ls /opt/mongodb/apk_packages/)
do
    apk add --no-cache /opt/mongodb/apk_packages/$i
done