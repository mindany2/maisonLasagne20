#!/bin/sh

sudo rm ./web_app/logs/error.log
sudo systemctl reload apache2
curl 192.168.1.13 > /dev/null
cat web_app/logs/error.log
tail -f web_app/logs/error.log

