from tree.Bouton import Bouton
from tree.Style import Style
from flask import redirect, url_for



class Bouton_html(Bouton):
    """
    le bouton de l'application web
    """

    def __init__(self, nom, nom_env, position):
        Bouton.__init__(self, nom)
        self.nom_env = nom_env
        self.style_on = Style(position, "green")
        self.style_off = Style(position)
        self.style = self.style_off

    def change(self):
        Bouton.change(self)
        self.style = (self.style_off, self.style_on)[self.etat]


    def get_name(self):
        return self.nom_env+"."+ self.nom




