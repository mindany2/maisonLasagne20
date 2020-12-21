"""
This is the code run by apache
"""
import sys
import os 
sys.path.insert(0, '/home/pi/maison')

PATH = os.path.dirname(os.path.realpath(__file__))

from data_manager.read_html.configure_html import config_html
from web_app.buttons.Site_manager import Site_manager
from web_app.App import App

manager = Site_manager()
config_html(manager, PATH)

manager.build()

app = App(manager)

application = app.get_site()
