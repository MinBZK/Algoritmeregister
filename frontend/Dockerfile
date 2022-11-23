FROM harbor.cicd.s15m.nl/ictu-devops-docker-hub/library/node:19-alpine

ENV APP_ROOT /app

COPY ./frontend/.output /app
CMD node /app/server/index.mjs

# Expose ports
EXPOSE 3000:3000