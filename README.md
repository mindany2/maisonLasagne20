# HOME Scenarii project

This project allows you to control like with scenarii many devices on your home.
You can control these scenarii with a web app or even with power switch in the house.

# What did it does ?
It is possible to like your led strip controler, dmx controller, power switch in the home,
make all your light dimmable, control your pc remotelly, and even manage spotify with it.
You can create several environnements that have presets link with modes to manage your home as you want.
All scenario and web app page are entirely customasable.
See the data wiki for more informations.

# Installation
In a rpi, just do :
'''bash
sudo ./setup.sh
'''
Then, reboot your rpi and try 
'''bash
./see_log_tree.sh
'''
To relaunch the process just
'''bash
./launch.sh
'''
for spotify, st_nucleo, or pc installation see the wiki

setup pc_control:
create a shortcut of Main_PC_control.pyw in startup folder, do not forget to install pynput in the RIGHT version
wake_on_lan : bios setup, peripheral setup, remove fast startup on power settings
