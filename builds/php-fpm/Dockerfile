#
#--------------------------------------------------------------------------
# Image Setup
#--------------------------------------------------------------------------
FROM php:7.2-fpm

#
#--------------------------------------------------------------------------
# Software's Installation
#--------------------------------------------------------------------------
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
      default-mysql-client \
      zlib1g-dev \
      libxslt-dev \
      libicu-dev

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN apt-get update && \
    apt-get install -y ssh-client

#
#--------------------------------------------------------------------------
# Install the PHP extentions
#--------------------------------------------------------------------------
RUN docker-php-ext-install iconv \
#    mcrypt \
    mbstring \
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
    gettext \
    && pecl install xdebug \
    && docker-php-ext-enable xdebug

#---------------------------- NODEJS ------------------------
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt install -y nodejs

#---------------------------- RUBY ------------------------
RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests \
    curl \
    bzip2 \
    build-essential \
    libssl-dev \
    libreadline-dev \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/* && \
    curl -L https://github.com/sstephenson/ruby-build/archive/v20180329.tar.gz | tar -zxvf - -C /tmp/ && \
    cd /tmp/ruby-build-* && ./install.sh && cd / && \
    ruby-build -v 2.5.1 /usr/local && rm -rfv /tmp/ruby-build-* && \
    gem install bundler --no-rdoc --no-ri

RUN apt-get update
RUN apt-get install -y msmtp \
    mailutils

EXPOSE 9000

CMD ["php-fpm"]
