#!/bin/sh

sudo rm ./logs/*.log
sudo systemctl stop apache2.service
echo "apache2 : stopped"
sudo supervisorctl stop inter
sudo supervisorctl stop tree
sudo supervisorctl start tree
sudo supervisorctl start inter
sudo systemctl start apache2.service
echo "apache2 : started"
sleep 2
cat logs/tree.log
tail -f ./logs/tree.log

#cat logs/site.log
#tail -f ./logs/site.log
