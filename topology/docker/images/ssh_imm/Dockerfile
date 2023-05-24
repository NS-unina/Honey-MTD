FROM ubuntu:latest

RUN apt update && apt install  openssh-server sudo -y && apt-get install -y net-tools && apt-get install -y iproute2 && apt-get install -y iputils-ping

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 test 

RUN  echo 'test:test' | chpasswd

RUN service ssh start

EXPOSE 22

CMD ["/usr/sbin/sshd","-D","-p"]

