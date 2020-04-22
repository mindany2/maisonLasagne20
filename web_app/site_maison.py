from flask import Flask, redirect, url_for, request, render_template
from web_app.Formulaire import Formulaire
from web_app.boutons.Liste_boutons_html import Liste_boutons_html
from time import sleep

class Site_maison:
    """
    Définit l'intégralité du site
    """
    def  __init__(self):
        self.site = Flask(__name__)

        """
        Page d'accueil
        """
        @self.site.route('/', methods=['post', 'get'])
        def index():
            # liste_info est remplit directement dans bouton
            form = Formulaire()
            # on initialise toutes les datas
            if form.is_submitted():
                # on cherche le bouton qui à été appuyer
                for bouton in form:
                    if (bouton.data):
                        bt = Liste_boutons_html().get_bouton(str(bouton.data))
                        bt.press()
                        break

            # on reload tous les boutons
            for bt in Liste_boutons_html():
                bt.reload()
                        

            for bouton in form:
                bouton.data = bouton.name

            # permet de ne pas avoir le popup de verification de l'envoi
            if form.validate_on_submit():
                return redirect(url_for("index"))

            for bouton in form:
                print(bouton.id)
            return render_template("index.html", form = form, liste = Liste_boutons_html())


if __name__ == "__main__":
    site = Site_maison()
    site.site.run(debug = True)
   
