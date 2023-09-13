FROM php:8.2-apache
COPY src/ /var/www/html
RUN rm -f /var/www/html/psyduck.db
RUN mkdir /var/www/data && \
    chown www-data:www-data /var/www/data