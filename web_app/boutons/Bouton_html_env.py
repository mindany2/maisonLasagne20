from tree.Tree import Tree
from web_app.boutons.Style import Style
from web_app.boutons.Bouton_html import Bouton_html
from flask import redirect, url_for



class Bouton_html_env(Bouton_html):
    """
    le bouton de l'application web
    """

    def __init__(self, bouton, position):
        Bouton_html.__init__(self, bouton, Style(position, couleur="green"), Style(position))

    def get_id(self):
        return self.bouton.env.nom + "."+ self.bouton.preset.nom + "."+ self.bouton.nom

