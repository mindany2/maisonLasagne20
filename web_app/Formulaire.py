from flask_wtf import Form
from wtforms import StringField
from tree.Tree import Tree
from web_app.boutons.Liste_boutons_html import Liste_boutons_html
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

        bt = Liste_boutons_html().get_bouton(nom.label.text)
        return HTMLString('<button {params}>{label}</button>'.format(
            params=self.html_params(name=nom.name, style = bt.style, **kwargs),
            label=bt.get_name()))



class Widget(StringField):
    widget = Boutons()

class Formulaire(Form):
    class Meta:
            csrf = False
    #on génère la liste des boutons html
    for bt in Liste_boutons_html():
        vars()[bt.get_id()] = Widget(bt.get_id())




