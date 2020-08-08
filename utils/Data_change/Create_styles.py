from tree.boutons.html.style.Style import Style
from tree.boutons.html.style.Gradient import Gradient

def set_styles(env, preset):
    """
    met a jour tous les styles de la preset pour avoir de joli boutons
    """
    nb_boutons = len(preset.liste_boutons_html)
    liste_couleur = env.couleurs[1].generate_array(env.couleurs[0], nb_boutons+1)
    diff_position = -5
    taille_caractère = 17
    for i, bt in enumerate(preset.liste_boutons_html):
        grad = Gradient(liste_couleur[i],liste_couleur[i+1])
        nb_caractère = len(bt.nom)
        if i == 0:
            # le premier
            bt.style_off = Style(size = (taille_caractère*nb_caractère,50), background_image=grad,borders_radius_etat=(True, False),font_weight = "light",
                    borders_etat=(True, False))
            bt.style_on = Style(size = (taille_caractère*nb_caractère,50), background_image=grad,font_weight = "bolder", font_size = 23,
                    borders_radius_etat=(True, False), borders_etat=(True, False))
        elif i == nb_boutons-1:
            # le dernier
            bt.style_off = Style(size = (taille_caractère*nb_caractère,50), position = (0,diff_position*i),font_weight = "light",
                    background_image=grad,borders_radius_etat=(False, True), borders_etat=(False, True))
            bt.style_on = Style(size = (taille_caractère*nb_caractère,50), position = (0,diff_position*i),font_size = 23,
                    font_weight = "bolder",background_image=grad,borders_radius_etat=(False, True), borders_etat=(False, True))

        else:
            #les autres
            bt.style_off = Style(size = (taille_caractère*nb_caractère,50), position = (0,diff_position*i),font_weight = "light", background_image=grad)
            bt.style_on = Style(size = (taille_caractère*nb_caractère,50), position = (0,diff_position*i),
                    font_size = 23,font_weight = "bolder",background_image=grad)


