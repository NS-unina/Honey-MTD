#!/bin/sh

sudo su - cowrie1<<EOF
. cowrie/cowrie-env/bin/activate
cd cowrie 
bin/cowrie start
EOF
