FROM node:16.13.0

WORKDIR /app/frontend

COPY package*.json ./

RUN npm install

COPY . .

ENV PORT=8080

EXPOSE 8080

CMD ["npm", "start"]

#Docker Commands:
#docker build -t kit-frontend .
#docker run -p 3000:8080 kit-frontend 
#docker kill $(docker ps -q) --> kills all containers
