from flask_wtf import Form
from wtforms import StringField
from wtforms.widgets import HTMLString, html_params
from web_app.Client_statique import Client_statique


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

        tree = Client_statique.get_client()

        nom_env = nom.label.text.split("_")[0]
        index = int(nom.label.text.split("_")[1])
        nom_bt,style_bt = tree.send("get_bouton_html(\"{}\", {}).get_infos()".format(nom_env, index))
        return HTMLString('<button {params}>{label}</button>'.format(
            params=self.html_params(name=nom.name, style = style_bt, **kwargs),
            label=nom_bt))



class Widget(StringField):
    widget = Boutons()

class Formulaire(Form):
    tree = Client_statique.get_client()
    class Meta:
            csrf = False
    vars()["mode_0"] = Widget("mode_0")
    for nom_env in tree.send_request("get_noms_envi"):
        for i in range(0,10): # on met 10 boutons à dispo
            nom = nom_env + "_" + str(i)
            vars()[nom] = Widget(nom)



