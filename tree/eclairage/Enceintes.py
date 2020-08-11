
class Enceintes:
    """
    Gère une paire d'enceinte
    ( lier a une zone )
    """

    def __init__(self, nom, ampli, zone):
        self.nom = nom
        self.ampli = ampli
        self.zone = zone

    def change_volume(self, valeur):
        if self.ampli.etat():
            if valeur == 0:
                self.zone.set_power(0)
            elif valeur != 0 and self.zone.power == 0:
                self.zone.set_power(1)

            # si l'ampli est allumer
            self.zone.set_volume(valeur)
        self.zone.valeur = valeur
        self.zone.power = (valeur != 0)


