FROM ubuntu:14.04

MAINTAINER Damian Rusinek

# Install python, python3, pip
RUN apt-get update
RUN apt-get install -y build-essential 
RUN apt-get install -y python-dev python-pip
RUN apt-get install -y python3-dev python3-pip python-setuptools

RUN mkdir /opt/pas
WORKDIR /opt/pas