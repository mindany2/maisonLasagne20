git submodule update --init
sudo apt install python3-pip
sudo pip3 install -r requirements.txt
sudo pip3 install spotipy
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
sudo apt-get install supervisor
sudo apt-get install apache2
sudo apt-get install python3-smbus
sudo a2enmod wsgi
sudo apt-get install libatlas-base-dev
sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
sudo cp utils/dev_file/site_maison.conf /etc/apache2/sites-enabled/
sudo rm /etc/apache2/sites-enabled/000-default.conf
sudo cp utils/dev_file/supervisor/maison.conf /etc/supervisor/conf.d/
sudo cp utils/dev_file/raspotify /etc/default/raspotify
echo "now reboot and it is ok"
