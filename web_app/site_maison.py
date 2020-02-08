from flask import Flask, redirect, url_for, request, render_template

class Site_maison:
    """
    Définit l'intégralité du site
    """
    def  __init__(this):
        this.site = Flask(__name__)

        """
        Page d'accueil
        """
        @this.site.route('/')
        def index():
            return render_template("index.html")

    
"""
Ceci est le code qui sera éxécuter au lancement du site par apache
donc au démarage du rasperry
"""
site = Site_maison()

# on donne à apache la bonne application
app = site.site
