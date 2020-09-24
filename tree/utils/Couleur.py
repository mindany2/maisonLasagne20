import numpy as np

def rgb_to_hexa(r, g, b):
    return "0x"+hex(r)[2:4].zfill(2)+hex(g)[2:4].zfill(2)+hex(b)[2:4].zfill(2)

class Couleur:
    """
    Permet d'avoir la couleur en rgb
    """
    def __init__(self, entier):
        try:
            self.valeur = "0x"+(8-len(hex(entier)))*"0"+hex(entier)[2:]
        except:
            self.valeur = entier

    def set(self, couleur):
        self.valeur = couleur.valeur

    def int_to_rgb(self):
        self.r = int("0x"+self.valeur[2:4].zfill(2),16)
        self.g = int("0x"+self.valeur[4:6].zfill(2),16)
        self.b = int("0x"+self.valeur[6:8].zfill(2),16)
        return [self.r, self.g, self.b]

    def get_liste(self, variable_init, variable_self, nb_points):
        if variable_init != variable_self:
            return np.arange(variable_init, variable_self, float((variable_self - variable_init))/nb_points)
        return [variable_init]*nb_points

    def __str__(self):
        return str(self.valeur)

    def get_with_hash(self):
        return "#"+str(self.valeur)[2::]

    def __eq__(self, other):
        return int(self.valeur,16) == int(other.valeur,16)

    def generate_array(self, couleur_init, nb_points):
        self.int_to_rgb()
        couleur_init.int_to_rgb()
        liste_rouge = self.get_liste(couleur_init.r, self.r, nb_points)
        liste_vert = self.get_liste(couleur_init.g, self.g, nb_points)
        liste_bleu = self.get_liste(couleur_init.b, self.b, nb_points)
        return [rgb_to_hexa(int(r),int(g),int(b)) for r,g,b in zip(liste_rouge, liste_vert, liste_bleu)]

    def is_black(self):
        return int(self.valeur,16) == 0
    



