FROM nginxinc/nginx-unprivileged:1.21.6-alpine_devops

USER root

RUN apk update
RUN apk upgrade
RUN rm /etc/nginx/conf.d/default.conf
COPY ./frontend-beheer-2024/dist /app/webformulier2024
COPY ./frontend-beheer-2024/nginx /etc/nginx
CMD nginx -g "daemon off;"

# Expose ports
EXPOSE 8080:8080