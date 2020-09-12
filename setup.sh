git submodule update --init
sudo apt install python3-pip
sudo pip3 install -r requirements.txt
sudo apt-get install supervisor
sudo apt-get install apache2
sudo cp utils/dev_file/site_maison.conf /etc/apache2/sites-enabled/
sudo rm /etc/apache2/sites-enabled/000-default.conf
sudo cp utils/dev_file/supervisor/maison.conf /etc/supervisor/conf.d/
echo "now reboot and it is ok"
