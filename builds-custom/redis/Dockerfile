FROM redis:6.2

COPY ./config/redis.conf /usr/local/etc/redis/redis.conf
COPY ./config/init.sh ./
RUN chmod +x init.sh

#CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]