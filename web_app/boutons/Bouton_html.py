from tree.Tree import Tree
from web_app.boutons.Style import Style
from flask import redirect, url_for



class Bouton_html:
    """
    le bouton de l'application web
    """

    def __init__(self, bouton, style_on, style_off):
        self.bouton = bouton
        self.style_on = style_on
        self.style_off = style_off
        self.style = (self.style_off, self.style_on)[self.bouton.etat()]

    def press(self):
        self.bouton.press()

    def reload(self):
        self.style = (self.style_off, self.style_on)[self.bouton.etat()]

    def get_name(self):
        return self.bouton.nom

    def get_id(self):
        return self.bouton.nom

    def show(self):
        print(self.get_name() + " = " + str(self.bouton.etat()))




