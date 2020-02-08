from flask import Flask, redirect, url_for, request, render_template
import Home 

class Site_maison:
    """
    Définit l'intégralité du site
    """
    def  __init__(this, maison):
        this.site = Flask(__name__)
        this.maison = maison

        """
        Page d'accueil
        """
        @this.site.route('/')
        def index():
            return render_template("index.html")

   
