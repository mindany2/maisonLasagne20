#!/bin/sh
curl 192.168.1.13 > /dev/null
cat ./logs/site.log
tail -f ./logs/site.log
