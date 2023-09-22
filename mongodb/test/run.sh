#!/bin/bash

exec mongod --auth &
exec mongoimport --username root --password example --authenticationDatabase admin  --jsonArray --db=log_viewer_db --collection=sources --drop --file /tmp/test/test_seed.json