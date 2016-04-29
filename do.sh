#!/bin/bash

#if there is no cert, run:
#openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/nginx.key -out nginx/nginx.crt

docker stop http2
docker rm http2
docker rmi nginx
docker build -t nginx .
docker run  --name http2\
			-p 8080:8080\
            -v "/Users/jannik/Google Drive/Uni/Studienarbeit HTTP2/docker http2/data":/data\
            -d\
            nginx


            # --dns=192.168.99.100\
            # --dns-search=http2.dev\
            # -h http2.dev\
            # -p 192.168.99.100:443:443\
            # -p 192.168.99.100:80:80\