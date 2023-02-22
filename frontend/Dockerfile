# Build Image
FROM --platform=$BUILDPLATFORM node:11 AS builder

WORKDIR /usr/src/

# Copy package.json and package.lock.json
COPY package*.json ./

# Installs dependencies
RUN npm ci

# Copy public directory
COPY public/ public/
# Copies source directory
COPY src/ src/
# Copies TypeScript config
COPY tsconfig.json .
# Copies environment variables. These are injected during the build.
COPY .env .

# Runs npm `build` script
RUN npm run build

# Installs `serve` package in local directory.
RUN npm install -g --prefix ./serve serve@13

# Runtime image
FROM node:11-alpine AS runtime

WORKDIR /usr/src/

COPY --from=builder /usr/src/build/ build/
COPY --from=builder /usr/src/serve/ serve/

# Add embedded user and make them the owner of /usr/src/
RUN adduser --disabled-password frontend
RUN chown frontend -R .

USER frontend

EXPOSE 3000

ENTRYPOINT [ "./serve/bin/serve", "build" ]