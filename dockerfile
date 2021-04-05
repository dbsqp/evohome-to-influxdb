ARG ARCH=

# Pull base image
FROM ubuntu:latest

# Labels
LABEL MAINTAINER="https://github.com/dbsqp/"

# Setup external package-sources
RUN apt-get update && apt-get install -y \
    ruby-full \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* &&
RUN gem install httparty -v 0.15.6 && \
    gem install evohome -v 1.0.0 && \
    gem install influxdb-client -v 1.12.1 && \
    gem install bundler -v 2.2.15 &&

# Environment vars
ENV LANG=C.UTF-8

# Copy files
COPY Gemfile evohome2influx.rb get.sh

# Run
CMD ["/bin/bash","/get.sh"]
