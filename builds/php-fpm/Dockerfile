#--------------------------------------------------------------------------
# Image Setup
#--------------------------------------------------------------------------
#FROM php:8.1.0-fpm
FROM php:8.1-fpm

#--------------------------------------------------------------------------
# Software's Installation
#--------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y \
      cron\
      git \
      gzip \
      libbz2-dev \
      libfreetype6-dev \
      libicu-dev \
      libjpeg62-turbo-dev \
      libmagickwand-dev \
      libmcrypt-dev \
      libonig-dev \
      libpng-dev \
      libsodium-dev \
      libssh2-1-dev \
      libwebp-dev \
      libxslt1-dev \
      libzip-dev \
      libpq-dev \
      libjpeg-dev \
      libssl-dev \
      libmagickwand-dev \
      libxml2-dev \
      default-mysql-client \
      zlib1g-dev \
      ssh-client \
      vim \
      procps

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

#--------------------------------------------------------------------------
# Install the PHP extentions
#--------------------------------------------------------------------------
RUN docker-php-ext-install iconv \
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
    intl \
    pdo_mysql \
    soap \
    xsl \
    gettext \
    pcntl

RUN docker-php-ext-configure gd --with-freetype=/usr/include/ --with-jpeg=/usr/include/ \
    && docker-php-ext-install gd \
    && docker-php-ext-configure intl \
    && pecl install xdebug \
    && docker-php-ext-enable xdebug
#--------------------------------------------------------------------------
# MCRYPT
#----------------------------  ------------------------
#RUN apt-get update && apt-get install -y libmcrypt-dev \
#    && pecl install mcrypt-1.0.3 \
#    && docker-php-ext-enable mcrypt

#--------------------------------------------------------------------------
# IMAGE MAGIC
#----------------------------  ------------------------
RUN apt-get update && apt-get install -y libmagickwand-6.q16-dev --no-install-recommends \
 && ln -s /usr/lib/x86_64-linux-gnu/ImageMagick-6.8.9/bin-Q16/MagickWand-config /usr/bin \
 && pecl install imagick \
 && echo "extension=imagick.so" > /usr/local/etc/php/conf.d/ext-imagick.ini

#--------------------------------------------------------------------------
# NODEJS
#--------------------------------------------------------------------------
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
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
  && docker-php-ext-install zip

#--------------------------------------------------------------------------
# NODEJS & GRUNT
#--------------------------------------------------------------------------
RUN apt-get install -y nodejs
RUN curl https://www.npmjs.com/install.sh | sh
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
RUN pecl install ssh2-1.3.1
RUN docker-php-ext-enable ssh2

EXPOSE 9000
CMD ["php-fpm"]
