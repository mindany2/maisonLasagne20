from web_app.site_maison import Site_maison

class Home:
    """
    Classe contenant tous les éléments
    et gérant le lien entre toutes les classes
    """

    def __init__(this):
        this.site = Site_maison(this)


 
"""
Ceci est le code qui sera éxécuter au lancement du site par apache
donc au démarage du rasperry
"""
# on lance tout avec la classe Maison
maison = Home()


# on donne à apache la bonne application
app = maison.site.site
