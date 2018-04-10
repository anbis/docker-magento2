FROM anbis/quick-magento2-php-fpm-ioncube

RUN apt-get update \
  && apt-get install -y \
    git

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["php-fpm", "-F"]
