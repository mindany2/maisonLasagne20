from tree.Bouton import Bouton
from tree.Tree import Tree
from web_app.Style import Style
from flask import redirect, url_for



class Bouton_html:
    """
    le bouton de l'application web
    """

    def __init__(self,nom_env, bouton, position):
        self.bouton = bouton
        self.nom_env = nom_env
        self.style_on = Style(position, "green")
        self.style_off = Style(position)
        self.style = (self.style_off, self.style_on)[self.bouton.etat]

    def reload(self):
        self.style = (self.style_off, self.style_on)[self.bouton.etat]

    def get_name(self):
        return self.nom_env+"."+ self.bouton.nom

    def show(self):
        print(self.get_name() + " = " + str(self.bouton.etat))




