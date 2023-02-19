FROM node:17-alpine

COPY . .
WORKDIR /app

# install node modules 
RUN npm i
#build app
RUN npm run build

# expose port 
EXPOSE 3000
# start app
CMD ["npm", "start"]

HEALTHCHECK --interval=10s --timeout=3s \
    CMD curl -f http://localhost/ || exit 1
