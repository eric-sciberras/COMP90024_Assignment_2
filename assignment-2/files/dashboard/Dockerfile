FROM node:12.16.3-alpine3.11

USER root

# Define environment variables
ENV APP_DIR /usr/src/app
ENV PORT 80
ENV COUCHDB_URL localhost
ENV COUCHDB_PORT 5984
ENV COUCHDB_USERNAME admin
ENV COUCHDB_PASSWORD password

# Creating Application dir
RUN mkdir -p $APP_DIR

# Defining workdir
WORKDIR $APP_DIR

COPY package*.json ./
RUN npm ci

COPY . .

CMD [ "node", "bin/www" ]

EXPOSE $PORT
