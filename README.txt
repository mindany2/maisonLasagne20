Sportify : 
https://pimylifeup.com/raspberry-pi-spotify/

Installation:
Open i2c, serial port : sudo raspi-config

sudo apt update
sudo apt full-upgrade
sudo apt install git
ssh-keygen -t rsa -b 4096 -C "leo.dupontrenoux@gmail.com"
cat .ssh/id_rsa.pub
git clone git@github.com:lasagne20/maison.git
sudo apt install python3-pip
sudo pip3 install -r requirements.txt
sudo apt install supervisor
