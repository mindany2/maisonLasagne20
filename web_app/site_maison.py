from flask import Flask, redirect, url_for, request, render_template
from web_app.Formulaire import Formulaire
from web_app.Client_statique import Client_statique
from time import sleep

class Site_maison:
    """
    Définit l'intégralité du site
    """
    def  __init__(self):
        self.site = Flask(__name__)
        tree = Client_statique.get_client()

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
                        #print(bouton.data)
                        nom_env = bouton.data.split("_")[0]
                        index = int(bouton.data.split("_")[1])
                        tree.send_request("press_bouton_html", [nom_env, index])
                        break

            # on reload tous les boutons
            tree.send_request("reload_html")
                        

            for bouton in form:
                bouton.data = bouton.name

            # permet de ne pas avoir le popup de verification de l'envoi
            if form.validate_on_submit():
                return redirect(url_for("index"))

            return render_template("index.html", form = form, tree = tree)


if __name__ == "__main__":
    site = Site_maison()
    site.site.run(debug = True)
   
