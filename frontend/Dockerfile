# syntax=docker/dockerfile:1

FROM node:16-alpine
WORKDIR /frontend
COPY . .
RUN npm ci
RUN npm run build
EXPOSE 3000
CMD [ "npx", "serve", "build" ]
