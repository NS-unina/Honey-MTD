#!/bin/bash

echo "CHECK"
echo $1
echo $2
nmap -sT $1 -vvv -oN "./Prove12/Prova6/prova$2.txt"
