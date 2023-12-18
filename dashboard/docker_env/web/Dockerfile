#FROM registry.cn-zhangjiakou.aliyuncs.com/dvadmin-pro/node12-base-web:latest
FROM node:18.14.2-alpine
WORKDIR /web/
COPY web/. .
#RUN npm cache clean -f
ENV NODE_OPTIONS=--openssl-legacy-provider
RUN npm install --registry=https://registry.npm.taobao.org
RUN npm run build

FROM nginx:alpine
COPY ./docker_env/nginx/my.conf /etc/nginx/conf.d/my.conf
COPY --from=0 /web/dist /usr/share/nginx/html
