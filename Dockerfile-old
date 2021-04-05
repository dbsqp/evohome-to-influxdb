ARG ARCH=
FROM ruby:2.4.2
RUN mkdir /usr/src/app
ADD . /usr/src/app/
WORKDIR /usr/src/app/
COPY Gemfile .
#COPY Gemfile.lock .
RUN chown -R nobody:nogroup .
RUN bundle install
COPY main.rb .
CMD ["ruby", "/usr/src/app/main.rb"]
