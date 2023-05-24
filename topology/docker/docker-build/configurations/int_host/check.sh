#!/bin/bash

echo "CHECK"
echo $1
echo $2
nmap -sT $1 -vvv -oN "./Prova15/prova$2.txt"
