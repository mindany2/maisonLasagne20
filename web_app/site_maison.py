from flask import Flask, redirect, url_for, request, render_template
from tree.Tree import Tree
from web_app.Formulaire import Formulaire

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
                for bouton in form:
                    if (bouton.data):
                        nom = str(bouton.data)
                        nom_env = nom.split(".")[0]
                        nom_bouton = nom.split(".")[1]
                        # on fait les instructions
                        bt = Tree().get_bouton(nom_env, nom_bouton)
                        bt.do()
                        #on change les boutons radios
                        Tree().get_env(nom_env).change_select(bt)
                        break
                        

            compteur = 1
            for bouton in form:
                bouton.data = bouton.name
                compteur += 1

            # permet de ne pas avoir le popup de verification de l'envoi
            if form.validate_on_submit():
                return redirect(url_for("index"))


            return render_template("index.html", form = form)


if __name__ == "__main__":
    site = Site_maison()
    site.site.run(debug = True)
   
