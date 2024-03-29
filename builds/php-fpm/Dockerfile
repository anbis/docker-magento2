#--------------------------------------------------------------------------
# Image Setup
#--------------------------------------------------------------------------
FROM php:7.0-fpm

#--------------------------------------------------------------------------
# Software's Installation
#--------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      git \
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
      libicu-dev \
      ssh-client

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer --version=1.10.21

#--------------------------------------------------------------------------
# Install the PHP extentions
#--------------------------------------------------------------------------
RUN docker-php-ext-install iconv \
    mcrypt \
    mbstring \
    bcmath \
    bz2 \
    calendar \
    exif \
    mysqli \
    sockets \
    sysvmsg \
    sysvsem \
    sysvshm \
    opcache \
    xmlrpc \
    intl \
    pdo_mysql \
    soap \
    xsl \
    gettext \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install gd \
    && docker-php-ext-configure intl

#--------------------------------------------------------------------------
# XDEBUG
#--------------------------------------------------------------------------
RUN pecl install xdebug-2.7.2 \
    && docker-php-ext-enable xdebug
#--------------------------------------------------------------------------
# IMAGE MAGIC
#--------------------------------------------------------------------------
RUN apt-get update && apt-get install -y libmagickwand-6.q16-dev --no-install-recommends \
 && ln -s /usr/lib/x86_64-linux-gnu/ImageMagick-6.8.9/bin-Q16/MagickWand-config /usr/bin \
 && pecl install imagick \
 && echo "extension=imagick.so" > /usr/local/etc/php/conf.d/ext-imagick.ini

#--------------------------------------------------------------------------
# NODEJS
#--------------------------------------------------------------------------
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt install -y nodejs

#--------------------------------------------------------------------------
# MAILHOG
#--------------------------------------------------------------------------
ADD ./mhsendmail_linux_amd64 /usr/local/bin/
RUN mv /usr/local/bin/mhsendmail_linux_amd64 /usr/local/bin/mhsendmail
RUN chmod +x /usr/local/bin/mhsendmail

#--------------------------------------------------------------------------
# RUBY
#--------------------------------------------------------------------------
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

#--------------------------------------------------------------------------
# ZIP
#--------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libzip-dev \
        zip \
  && docker-php-ext-configure zip --with-libzip \
  && docker-php-ext-install zip

#--------------------------------------------------------------------------
# NODEJS & GRUNT
#--------------------------------------------------------------------------
RUN apt-get install -y nodejs
RUN apt-get install -y npm
RUN npm install grunt -g grunt-cli

#--------------------------------------------------------------------------
# UNZIP
#--------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    zip unzip

#--------------------------------------------------------------------------
# SSH2
#--------------------------------------------------------------------------
RUN apt-get update
RUN apt-get install -y libssh2-1-dev
RUN pecl install ssh2-1.2
RUN docker-php-ext-enable ssh2

EXPOSE 9000
CMD ["php-fpm"]
