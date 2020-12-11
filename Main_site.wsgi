"""
This is the code run by apache
"""
import sys
sys.path.insert(0, '/home/pi/maison')
from data_manager.read_html.configure_html import config_html
from web_app.buttons.Site_manager import Site_manager
from web_app.App import App

manager = Site_manager()
config_html(manager)

manager.build()

app = App(manager)

application = app.get_site()

application.run()
