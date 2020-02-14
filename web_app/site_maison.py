from flask import Flask, redirect, url_for, request, render_template
from tree.Liste_boutons import Liste_boutons
from tree.Liste_environnements import Liste_environnements

class Site_maison:
    """
    Définit l'intégralité du site
    """
    def  __init__(self):
        self.site = Flask(__name__)
        self.liste_envi = None

        """
        Page d'accueil
        """
        @self.site.route('/')
        def index():
            # liste_info est remplit directement dans bouton
            print(self.liste_envi.liste_info)
            return render_template("index.html", valeur = self.liste_envi.liste_info)

   
