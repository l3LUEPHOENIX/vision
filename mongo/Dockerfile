# Inspired by: https://github.com/mvertes/docker-alpine-mongo/blob/master/Dockerfile
FROM alpine:3.8

RUN mkdir /opt/ \
    && mkdir /opt/mongodb 
WORKDIR /opt/mongodb
COPY . .
RUN mkdir /data && \
    mkdir /data/db && \
    sh ./apk_packages/install_packages.sh
CMD ["sh", "./run.sh"]