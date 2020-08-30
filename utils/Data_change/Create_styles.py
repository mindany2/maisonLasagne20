from tree.boutons.html.style.Style import Style
from tree.boutons.html.style.Gradient import Gradient
from copy import copy

def set_styles(env, preset):
    """
    met a jour tous les styles de la preset pour avoir de joli boutons
    """
    nb_boutons = len(preset.liste_boutons_html)
    liste_couleur = env.couleurs[1].generate_array(env.couleurs[0], nb_boutons+1)
    taille_caractère = 11
    for i, bt in enumerate(preset.liste_boutons_html):
        grad = Gradient(liste_couleur[i],liste_couleur[i+1])
        nb_caractère = len(bt.nom)

        style = Style(size = (taille_caractère*nb_caractère,50),
                    background_image=grad,
                    margin = [-5, 0])


        bt.style_off = copy(style)
        bt.style_off.font_weight = "light"
        bt.style_off.font_size = 10

        bt.style_on = copy(style)
        bt.style_on.font_weight = "bolder"
        bt.style_on.font_size = 18

        if i == 0:
            print("premier : "+bt.nom)
            # le premier
            bt.style_off.set_border((True, False),(True, False))
            bt.style_on.set_border((True, False),(True, False))

        elif i == nb_boutons-1:
            print("dernier : "+bt.nom)
            # le dernier
            bt.style_off.set_border((False, True),(False, True))
            bt.style_on.set_border((False, True),(False, True))
