FROM postgres:9.5
# FROM ubuntu:14.04
# RUN apt-get update && apt-get upgrade -y
# RUN apt-get update && apt-get install -y wget  
# install postgres9.5
# RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list
# RUN wget https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
# RUN apt-get update && apt-get -y install postgresql postgresql-contrib


RUN apt-get update && apt-get install -y \
	libpq-dev \
	python-pip \
	python-psycopg2 \
	wget \
	&& rm -rf /var/lib/apt/lists/*

RUN pip install Flask

RUN useradd -ms /bin/bash yifei

RUN whoami

RUN mkdir /home/yifei/.dockstore
RUN mkdir /home/yifei/.dockstore/self-install
RUN chmod 777 /home/yifei/.dockstore
COPY dockstore /
COPY config /
RUN mv /dockstore /home/yifei/.dockstore/
RUN mv /config /home/yifei/.dockstore/
RUN chmod -R 777 /home/yifei/.dockstore/
RUN export PATH=$PATH:/home/yifei/.dockstore/

USER yifei

EXPOSE 5000
CMD ~/.dockstore/dockstore && dockstore --version