FROM node:22-alpine
WORKDIR /app
COPY admin-frontend/package.json .
RUN npm install -f
COPY admin-frontend/ .
EXPOSE 8081
CMD ["npm", "run", "dev"]

