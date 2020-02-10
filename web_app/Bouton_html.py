from tree.Bouton import Bouton
from flask import redirect, url_for

class Bouton_html(Bouton):
    """
    le bouton de l'application web
    """

    def __init__(self, nom, page, app, liste_info):
        Bouton.__init__(nom)
        self.page = page
        self.app = app
        # liste_parametre[0] = faux / [1] = vrai
        self.liste_parametre = [[],[]]
        self.liste_info = self.liste_parametre[0]
        liste_info.append(self.liste_info)

        @this.app.route('/'+nom)
        def bouton():
            #on fait les instructions
            this.do()
            this.change()
            #on change la valeur de l'info
            self.liste_info = self.liste_parametre[self.etat]

            return redirect(url_for(page))

        def add_param(self, param_vrai, param_faux):
            self.liste_parametre[0].append(param_faux)
            self.liste_parametre[1].append(param_vrai)


