#
#--------------------------------------------------------------------------
# Image Setup
#--------------------------------------------------------------------------
#

FROM php:7.1.3-fpm

#
#--------------------------------------------------------------------------
# Software's Installation
#--------------------------------------------------------------------------
#

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
#        geoip-bin \
#        geoip-database \
#        libgeoip-dev \
      git \
#        libmemcached-dev \
      libz-dev \
      libpq-dev \
      libfreetype6-dev \
      libjpeg62-turbo-dev \
      libpng-dev \
      libjpeg-dev \
      libssl-dev \
      libmagickwand-dev \
      libmcrypt-dev \
      libxml2-dev \
      mysql-client \
      zlib1g-dev \
      libxslt-dev \
      libicu-dev

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

#
#--------------------------------------------------------------------------
# Install the PHP extentions
#--------------------------------------------------------------------------
#

RUN docker-php-ext-install iconv mcrypt mbstring \
    && docker-php-ext-install zip \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install gd \
    && docker-php-ext-configure intl \
    && docker-php-ext-install \
    bcmath \
    intl \
    pdo_mysql \
    soap \
    xsl \
    && pecl install xdebug \
    && docker-php-ext-enable xdebug

EXPOSE 9000

CMD ["php-fpm"]
