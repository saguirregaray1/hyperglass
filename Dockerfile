FROM python:3.12.3-alpine as base
WORKDIR /opt/hyperglass
ENV HYPERGLASS_APP_PATH=/etc/hyperglass
ENV HYPERGLASS_HOST=0.0.0.0
ENV HYPERGLASS_PORT=8001
ENV HYPERGLASS_DEBUG=false
ENV HYPERGLASS_DEV_MODE=false
ENV HYPERGLASS_REDIS_HOST=redis
ENV HYPEGLASS_DISABLE_UI=true
ENV HYPERGLASS_CONTAINER=true
ENV HTTP_PROXY="http://172.29.99.245:3128"
ENV HTTPS_PROXY="http://172.29.99.245:3128"
ENV SECRET_KEY="django-insecure-ets-bi835_vk0=3_9z1a39$(#fmq#4f=#%g9!@ry03yam#y+_f"
COPY . .

FROM base as ui
WORKDIR /opt/hyperglass/hyperglass/ui
RUN apk add build-base pkgconfig cairo-dev nodejs npm
RUN npm install -g pnpm
RUN pnpm install -P

FROM ui as hyperglass
WORKDIR /opt/hyperglass
RUN pip3 install -e .

EXPOSE ${HYPERGLASS_PORT}
CMD ["python3", "-m", "hyperglass.console", "start"]
