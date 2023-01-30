FROM node:17-alpine

COPY . .
WORKDIR /app

# install node modules 
RUN npm ci
#build app
RUN npm run build

# expose port 
EXPOSE 3000
# start app
CMD ["npm", "start"]
