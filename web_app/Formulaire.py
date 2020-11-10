from flask_wtf import Form
from wtforms import StringField
from wtforms.widgets import HTMLString, html_params
from web_app.Client_statique import Client_statique
from utils.communication.get.Get_infos_envs import Get_infos_envs
from utils.communication.get.Get_bt_html import Get_bt_html


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

        client = Client_statique.get_client()

        nom_env = nom.label.text.split("_")[0]
        index = int(nom.label.text.split("_")[1])
        nom_bt,style_bt = client.send(Get_bt_html(nom_env, index))
        return HTMLString('<button {params}>{label}</button>'.format(
            params=self.html_params(name=nom.name, style = style_bt, **kwargs),
            label=nom_bt))



class Widget(StringField):
    widget = Boutons()

class Formulaire(Form):
    client = Client_statique.get_client()
    class Meta:
            csrf = False
    vars()["mode_0"] = Widget("mode_0")
    for info_env in client.send(Get_infos_envs()):
        for i in range(0,10): # on met 10 boutons à dispo
            nom = info_env[0] + "_" + str(i)
            vars()[nom] = Widget(nom)



