from tree.boutons.html.style.Style import Style
from tree.boutons.html.style.Gradient import Gradient
from copy import copy

LONGUEUR = 80

def set_styles(env, preset):
    """
    met a jour tous les styles de la preset pour avoir de joli boutons
    """
    nb_boutons = len(preset.liste_boutons_html)
    liste_couleur = env.couleurs[1].generate_array(env.couleurs[0], nb_boutons+1)
    for i, bt in enumerate(preset.liste_boutons_html):
        grad = Gradient(liste_couleur[i],liste_couleur[i+1])
        nb_caractère = len(bt.nom)

        style = Style(size = (LONGUEUR,40),
                    background_image=grad,
                    margin = (-5, 0))

        bt.style_off = copy(style)
        bt.style_off.font_weight = "light"
        bt.style_off.font_size = 15

        bt.style_on = copy(style)
        bt.style_on.font_weight = "bolder"
        bt.style_on.font_size = 19

        if i == 0:
            # le premier
            bt.style_off.set_border((True, False),(True, False))
            bt.style_on.set_border((True, False),(True, False))

        elif i == nb_boutons-1:
            # le dernier
            bt.style_off.set_border((False, True),(False, True))
            bt.style_on.set_border((False, True),(False, True))

def set_env_style(env, liste_modes):
    # style de l'environnement
    for mode in liste_modes:
        nb_boutons = len(env.liste_presets_choisis.get(mode).liste_boutons_html)
        env.style.add(Style(position= (0, nb_boutons*LONGUEUR/2-len(env.nom)*4),
                        font_size = 18,
                        couleur_texte = mode.couleur,
                        nom = mode.nom,
                        font_weight = "bolder"))
