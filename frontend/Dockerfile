FROM node:20

WORKDIR /app

# зависимости
COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "start"]