from flask_wtf import Form
from wtforms import StringField
from tree.Tree import Tree
from web_app.Liste_boutons_html import Liste_boutons_html
from utils.Data_change.Create_tree import get_tree
from utils.Data_change.Create_html_boutons import get_liste
from wtforms.widgets import HTMLString, html_params


class Boutons(object):
    """
    ici la liste des boutons d'un environnement
    """
    input_type = 'submit'
    html_params = staticmethod(html_params)
    nom_bouton = None
    nom_env = None

    def __call__(self, nom, **kwargs):
        """
        pose les boutons
        """
        kwargs.setdefault('id', nom.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = nom._value()

        self.nom_env = nom.label.text.split(".")[0]
        self.nom_bouton = nom.label.text.split(".")[1]
        bt = Liste_boutons_html().get_bouton(nom.label.text)
        return HTMLString('<button {params}>{label}</button>'.format(
            params=self.html_params(name=nom.name, style = bt.style, **kwargs),
            label=self.nom_bouton))



class Widget(StringField):
    widget = Boutons()

class Formulaire(Form):
    class Meta:
            csrf = False
    # on génère l'arbre
    get_tree()
    #on génère la liste des boutons html
    liste = get_liste()
    for bt in liste:
        vars()[bt.get_name()] = Widget(bt.get_name())




