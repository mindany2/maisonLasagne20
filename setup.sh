git submodule update --init
sudo apt -y install python3-pip
sudo pip3 install -r requirements.txt
sudo pip3 install spotipy
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
sudo apt-get -y install supervisor
sudo apt-get -y install apache2
sudo apt-get -y install python3-smbus
sudo a2enmod wsgi
sudo apt-get -y install libatlas-base-dev
sudo apt-get -y install python3-pip apache2 libapache2-mod-wsgi-py3
sudo cp dev_file/site_maison.conf /etc/apache2/sites-enabled/
sudo rm /etc/apache2/sites-enabled/000-default.conf
sudo cp dev_file/supervisor/maison.conf /etc/supervisor/conf.d/
sudo cp dev_file/raspotify /etc/default/raspotify
mkdir logs
echo "now reboot and it is ok"
