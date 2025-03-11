FROM node:lts AS build

WORKDIR /app

COPY package.json .

RUN rm -rf node_modules
RUN npm install

COPY . .
RUN npm run build

FROM nginx:latest

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

# Add nginx config
# COPY nginx.conf /temp/prod.conf
# RUN envsubst /app < /temp/prod.conf > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
