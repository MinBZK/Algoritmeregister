FROM harbor.cicd.s15m.nl/ocw-lsp-pub/nginxinc/nginx-unprivileged:1.21.6-alpine_lsp

USER root
RUN apk update
RUN apk upgrade
RUN rm /etc/nginx/conf.d/default.conf
COPY ./frontend-beheer/dist /app/webformulier
COPY ./frontend-beheer/nginx /etc/nginx
CMD nginx -g "daemon off;"

# Expose ports
EXPOSE 8080:8080