#!/bin/sh

sudo ovs-vsctl del-br br0
sudo ovs-vsctl del-br br1
sudo netplan apply

