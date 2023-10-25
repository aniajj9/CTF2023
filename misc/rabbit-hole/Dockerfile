# Use the official PHP Apache image
FROM php:8.2-apache

# Copy your application files into the container
COPY ./public/ /var/www/html/
COPY ./private/ /srv/private/
COPY ./rewrite.conf /etc/apache2/conf-enabled/rewrite.conf

# Expose port 80 (Apache default)
EXPOSE 80


# Start Apache when the container runs
CMD ["apache2-foreground"]
