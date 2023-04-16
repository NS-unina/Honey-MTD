#!/bin/sh

sudo apt update
sudo apt -y install systemd
sudo apt -y install telnetd
sudo ufw allow 23/tcp
sudo useradd host
sudo passwd host

sudo apt -y install vsftpd
sudo service vsftpd enable
sudo service vsftpd start

sudo apt -y install apache2
sudo service apache2 enable
sudo service apache2 start
