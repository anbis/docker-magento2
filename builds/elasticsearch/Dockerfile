FROM docker.elastic.co/elasticsearch/elasticsearch:6.8.12

######### install plugin analysis and phonetic ################
RUN bin/elasticsearch-plugin install analysis-icu
RUN bin/elasticsearch-plugin install analysis-phonetic
###############################################################

USER root
RUN echo "vm.max_map_count=262144" >> /etc/sysctl.conf
