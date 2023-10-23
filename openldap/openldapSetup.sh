#!/bin/sh

ldapadd -x -w abc123 -H ldaps://localhost:1389 -D "cn=vision,dc=domain3,dc=local" -f /home/openldap/vision.ldif