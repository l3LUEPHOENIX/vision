#!/bin/bsh

key=$(cat /opt/vision/secrets/vision_key.txt | wc -m)
if [ $key -le 1 ]
then
    python3 ./vision_config_gen.py
fi
gunicorn --certfile /opt/vision/secrets/cert.pem --keyfile /opt/vision/secrets/key.pem app:app --worker-class gevent --bind 0.0.0.0:7443