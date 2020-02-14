#!/bin/sh

sudo systemctl reload apache2
curl -s http://192.168.1.13/ > /dev/null
cat web_app/logs/error.log | cut -d']' -f5
cat web_app/logs/error.log 
rm ./web_app/logs/error.log
touch ./web_app/logs/error.log

