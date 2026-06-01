FROM node:20-slim

WORKDIR /usr/src/app

COPY /tailwind/package*.json .

RUN npm ci

COPY . .

CMD ["npm", "run", "dev"]