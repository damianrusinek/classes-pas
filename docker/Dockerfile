FROM ubuntu:14.04

MAINTAINER Damian Rusinek

# Install python, python3, pip
RUN apt-get update
RUN apt-get install -y build-essential 
RUN apt-get install -y python-dev python-pip
RUN apt-get install -y python3-dev python3-pip python-setuptools
RUN apt-get install -y supervisor 
RUN apt-get install -y postfix 
RUN apt-get install -y mailutils
RUN apt-get install -y courier-imap

RUN useradd test -p pawpU97AVNPO6 -m
RUN maildirmake /home/test/Maildir
RUN chown -R test:test /home/test

ADD assets/configure.sh /opt/configure.sh
RUN chmod u+x /opt/configure.sh

RUN mkdir /opt/pas
WORKDIR /opt/pas

CMD /opt/configure.sh;/usr/bin/supervisord -c /etc/supervisor/supervisord.conf