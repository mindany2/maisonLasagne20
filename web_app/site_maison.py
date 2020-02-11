from flask import Flask, redirect, url_for, request, render_template
from tree.Liste_boutons import Liste_boutons
from tree.Liste_environnements import Liste_environnements

class Site_maison:
    """
    Définit l'intégralité du site
    """
    def  __init__(this):
        this.site = Flask(__name__)
        this.liste_envi = Liste_environnements()

        """
        Page d'accueil
        """
        @this.site.route('/')
        def index():
            # liste_info est remplit directement dans bouton
            return render_template("index.html", valeur = this.liste_envi.liste_info)

   
