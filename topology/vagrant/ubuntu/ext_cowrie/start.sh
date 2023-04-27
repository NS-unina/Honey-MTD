#!/bin/sh

sudo su - cowrie1<<EOF
./conf.sh
. cowrie/cowrie-env/bin/activate
cd cowrie 
bin/cowrie start
EOF
