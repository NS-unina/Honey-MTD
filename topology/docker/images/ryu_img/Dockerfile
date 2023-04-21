FROM ubuntu:latest

RUN apt update && apt-get -y install python3-pip && apt-get -y install software-properties-common && apt-get -y install git
RUN apt-get install -y net-tools
RUN apt-get install -y iproute2
RUN apt-get install -y iputils-ping
RUN add-apt-repository ppa:deadsnakes/ppa
# export timezone - for python3.9-dev install
ENV TZ=Europe/London

# place timezone data /etc/timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install
RUN apt-get update && apt-get -y install --no-install-recommends python3.8 && apt-get -y install python3-pip
RUN pip install virtualenv
RUN virtualenv controller -p python3.8
RUN . controller/bin/activate
RUN apt-get -y install python3.8-distutils 
RUN pip install ryu
RUN pip install eventlet==0.30.2