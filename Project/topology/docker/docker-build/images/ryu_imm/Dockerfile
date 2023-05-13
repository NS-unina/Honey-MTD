FROM python:3.8.10

RUN apt update && apt-get -y install python3-pip && apt-get -y install software-properties-common && apt-get -y install git
RUN apt-get install -y net-tools
RUN apt-get install -y iproute2
RUN apt-get install -y iputils-ping
RUN pip install randmac
RUN pip install ryu
RUN pip install eventlet==0.30.2
