FROM ubuntu:14.04

MAINTAINER Damian Rusinek

# Install python, python3, pip
RUN apt-get update && apt-get install -y \
  build-essential \
  python-dev python-pip \
  python3-dev python3-pip python-setuptools \
  supervisor \
  postfix \
  mailutils \
  courier-imap \
  libffi-dev \
  libssl-dev \
  openssh-server \
  proftpd-basic \
  git

# Powinny byc uruchomione usługi: ssh, smtp, pop3

RUN useradd test -p pawpU97AVNPO6 -m # test:test
RUN maildirmake /home/test/Maildir
RUN chown -R test:test /home/test

ADD assets/configure.sh /opt/configure.sh
RUN chmod u+x /opt/configure.sh

RUN git clone https://github.com/ernw/knxmap.git /opt/knxmap
RUN cd /opt/knxmap && git checkout v0.9.0

RUN mkdir /opt/pas
WORKDIR /opt/pas


CMD /opt/configure.sh;/usr/bin/supervisord -c /etc/supervisor/supervisord.conf
