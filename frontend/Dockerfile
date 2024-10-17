FROM /node:21.4.0-alpine3.18

RUN addgroup -S nonroot && \
  adduser -S nonroot -G nonroot
USER nonroot

ENV APP_ROOT /app

COPY ./frontend/.output /app
CMD node /app/server/index.mjs

# Expose ports
EXPOSE 3000:3000