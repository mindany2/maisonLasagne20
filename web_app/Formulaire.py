from flask_wtf import Form
from wtforms import StringField
from tree.Tree import Tree
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


        nom_env = nom.label.text.split("_")[0]
        index = int(nom.label.text.split("_")[1])
        bt = Tree().get_bouton_html(nom_env, index)
        return HTMLString('<button {params}>{label}</button>'.format(
            params=self.html_params(name=nom.name, style = bt.style, **kwargs),
            label=bt.get_name()))



class Widget(StringField):
    widget = Boutons()

class Formulaire(Form):
    class Meta:
            csrf = False
    #on génère la liste des boutons html
    vars()["mode_0"] = Widget("mode_0")
    for env in Tree().liste_envi:
        for i in range(0,10): # on met 10 boutons à dispo
            nom = env.nom + "_" + str(i)
            vars()[nom] = Widget(nom)



