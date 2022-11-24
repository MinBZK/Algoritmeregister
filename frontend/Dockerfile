FROM harbor.cicd.s15m.nl/ictu-devops-pub/nginxinc/nginx-unprivileged:1.21.6-alpine_rid

USER root
RUN apk update
RUN apk upgrade

RUN apk add --update npm

COPY ./frontend/.output /app

RUN rm /etc/nginx/conf.d/default.conf

COPY ./frontend/nginx /etc/nginx

RUN node /app/server/index.mjs

CMD nginx -g "daemon off;"

# Expose ports
EXPOSE 8080:8080