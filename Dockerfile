FROM nginx:alpine

RUN mkdir -p /etc/ssl/certs/
RUN mkdir -p /etc/nginx/sites-enabled/

COPY nginx/nginx.crt /etc/ssl/certs/
COPY nginx/nginx.key /etc/ssl/certs/

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/http2.conf /etc/nginx/sites-enabled/http2.conf
