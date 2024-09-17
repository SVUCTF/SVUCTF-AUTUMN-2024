FROM ghcr.io/svuctf/base-v2/php-nginx:8.3

RUN apk add --no-cache zlib-dev libpng-dev && \
    docker-php-ext-install -j$(nproc) gd

COPY --chown=www-data html /var/www/html
