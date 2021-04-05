ARG ARCH=

# Pull base image
FROM ubuntu:latest

# Labels
LABEL MAINTAINER="https://github.com/dbsqp/"

# Setup external package-sources
RUN apt-get update && apt-get install -y \
    ruby \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* 

# Environment vars
# ENV PYTHONIOENCODING=utf-8

# Copy files
ADD Gemfile /
ADD evohome2influxdb.rb /
ADD get.sh /

# Run
CMD ["/bin/bash","/get.sh"]
