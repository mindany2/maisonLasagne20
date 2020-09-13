from enum import Enum
from tree.eclairage.Lumiere import Lumiere

class Lyre(Lumiere):
    """
    Une petite lyre en 11 channel
    """
    def __init__(self, nom, controleur):
        Lumiere.__init__(self, nom)
        self.dmx = controleur
        self.pan = 0
        self.tilt = 0
        self.vitesse_moteur = 0
        self.vitesse = 0
        self.strombo = 0

        self.couleur = COULEUR.blanc
        self.gobo = GOBO.rond

    def set_position(self, pan, tilt):
        self.pan = pan
        self.tilt = tilt
        self.dmx.set(CHANNEL.pan, pan)
        self.dmx.set(CHANNEL.tilt, tilt)

    def set_couleur(self, couleur):
        self.couleur = couleur
        self.dmx.set(CHANNEL.couleur, couleur.value)

    def set_gobo(self, gobo):
        self.gobo = gobo
        self.dmx.set(CHANNEL.gobo, gobo.value)

    def set_strombo(self, strombo):
        self.strombo = strombo
        self.dmx.set(CHANNEL.strombo, strombo)

    def set_dimmeur(self, dimmeur):
        self.dimmeur = dimmeur
        self.dmx.set(CHANNEL.dimmeur, dimmeur)

    def set_vitesse(self, vitesse):
        self.vitesse = vitesse
        self.dmx.set(CHANNEL.vitesse, vitesse)

    def set_vitesse_moteur(self, vitesse_moteur):
        self.vitesse_moteur = vitesse_moteur
        self.dmx.set(CHANNEL.vitesse_moteur, vitesse_moteur)


class COULEUR(Enum):
    # il manque les milieux
    blanc = 0
    rouge = 15
    orange = 25
    jaune = 37
    vert = 50
    bleu = 60
    cyan = 70
    violet = 80
    roue = 255

class GOBO(Enum):
    # il manque les gobos qui bougent
    rond = 0
    rond_casser = 20
    fleur = 40
    flocon = 50
    tag = 65
    points = 80
    tatouage = 95
    rayure = 110

class CHANNEL(Enum):
    pan = 1
    tilt = 2
    ajustment_pan = 3
    ajustment_tilt = 4
    vitesse_moteur = 5
    couleur = 6
    gobo = 7
    dimmeur = 8
    strombo = 9
    scene = 10
    vitesse = 11

