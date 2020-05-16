from web_app.site_maison import Site_maison
from time import sleep
"""
Ceci est le code qui sera éxécuter au lancement du site par apache
"""
site = Site_maison()



# on donne à apache la bonne application
app = site.site


if __name__ == "__main__":
    pass
