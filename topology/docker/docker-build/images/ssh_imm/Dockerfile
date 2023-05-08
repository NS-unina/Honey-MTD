FROM ubuntu:latest

RUN apt update && apt upgrade -y 
RUN apt install sudo openssh-server -y
RUN apt-get install net-tools -y && apt-get install iproute2 -y && apt-get install iputils-ping -y

RUN mkdir /var/run/sshd

RUN echo 'root:hellossh' | chpasswd

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' \
    /etc/ssh/sshd_config

#SSH login fix
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional \
    pam_loginuid.so@g' -i /etc/pam.d/sshd

#expose port 22
EXPOSE 22

#Commands to be executed by default
CMD ["/usr/sbin/sshd","-D"]