FROM php:8.2-apache

RUN apt-get update && \
    apt-get install -y netcat && \
    rm -rf /var/lib/apt/lists/*

ADD html/index.php /var/www/html/index.php
ADD secured /secured

RUN chown -R root:root /var/www/html

RUN chown -R root:root /secured && \
    chmod 0600 /secured/flag.txt && \
    chmod u+sx /secured/readflag
