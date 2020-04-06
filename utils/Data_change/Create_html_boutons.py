from tree.Tree import Tree
from web_app.Bouton_html import Bouton_html
from web_app.Liste_boutons_html import Liste_boutons_html

"""
Génère la liste des boutons html
"""

def get_liste():
    # on génère la liste des boutons
    liste = Liste_boutons_html()

    for i,env in enumerate(Tree().liste_envi):
        if env.have_html_boutons:
            for j,bt in enumerate(env.liste_boutons):
                liste.add_boutons(env.nom +"."+ bt.nom, Bouton_html(env.nom, bt, [i,j]))

    liste.show()
    return liste
