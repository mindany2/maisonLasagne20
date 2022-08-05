#!/bin/sh

sudo rm ./logs/inter.log
sudo supervisorctl stop inter
sudo supervisorctl start inter
sleep 1
cat logs/inter.log
tail -f ./logs/inter.log

