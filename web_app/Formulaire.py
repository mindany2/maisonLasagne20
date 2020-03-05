from flask_wtf import Form
from wtforms import StringField
from tree.Tree import Tree
from utils.In_out import get_tree
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
        envi = Tree().get_env(self.nom_env)
        bt = envi.get_bouton(self.nom_bouton)
        return HTMLString('<button {params}>{label}</button>'.format(
            params=self.html_params(name=nom.name, style = bt.style, **kwargs),
            label=self.nom_bouton))



class Widget(StringField):
    widget = Boutons()

class Formulaire(Form):
    class Meta:
            csrf = False
    tree = get_tree()
    for envi in Tree():
        for bt in envi.liste_boutons:
            vars()[envi.nom + "."+bt.nom] = Widget(bt.get_name())




