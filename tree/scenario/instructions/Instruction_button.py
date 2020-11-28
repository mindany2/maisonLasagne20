from tree.scenario.Instruction import Instruction
from tree.boutons.Bouton_secondaire import Bouton_secondaire
from tree.boutons.Bouton_principal import Bouton_principal
from tree.Tree import Tree
from utils.Logger import Logger
from enum import Enum

class TYPE_BOUTON(Enum):
    principal = 0
    secondaire = 1

class Instruction_bouton(Instruction):
    """
    Une instruction appellant un bouton d'un autre environnement
    """
    def __init__(self, nom_env, nom_preset, nom_scenars, type_bt, temps_init, synchro, condition):
        Instruction.__init__(self, 0, temps_init, synchro)
        self.nom_env = nom_env
        self.nom_preset = nom_preset
        self.nom_scenars = nom_scenars.split(",")
        self.type_bt = type_bt
        self.condition = condition

        self.bouton = None
        self.preset = None
        self.env = None

    def run(self, barrier = None):
        super().run()

        if self.bouton == None:
            self.get_bt()

        condition = self.eval(self.condition)
        # on verifie que l'on est dans la bonne preset selectionner, sinon on ne fait rien
        if(self.env.get_preset_select() == self.preset):
            if len(self.nom_scenars) == 1 and condition:
                # on fait le scenar que si la condition est remplie
                self.bouton.press()
            else:
                # sinon on fait le on ou le off suivant la condition
                # on a obligatoirement un scenario principal
                self.bouton.press(etat=condition)

    def get_bt(self):
        try:
            self.env = Tree.get_env(self.nom_env) 
            self.preset = self.env.get_preset(self.nom_preset)
            self.scenars = [self.preset.get_scenar(nom_scenar) for nom_scenar in self.nom_scenars]
            for scenar in self.scenars:
                assert(scenar)

        except:
            raise(Exception("Not found exeption le scenario {} dans l'environnement {} preset {} n'existe pas"
                .format(self.nom_scenars, self.nom_env, self.nom_preset)))

        if self.type_bt == TYPE_BOUTON.principal:
            scenar_off = None
            if (len(self.scenars) > 1):
                scenar_off = self.scenars[1]
            self.bouton = Bouton_principal(self.nom_env + "."+ self.nom_preset +"." + self.nom_scenars[0], self.env, self.scenars[0], scenar_off)
        elif self.type_bt == TYPE_BOUTON.secondaire:
            self.bouton = Bouton_secondaire(self.nom_env + "."+ self.nom_preset +"." + self.nom_scenars[0], self.env, self.scenars[0])
        else:
            raise(Exception("Erreur type bouton : {}".format(self.type_bt)))

    def finish(self):
        if self.type_bt == TYPE_BOUTON.secondaire:
            self.bouton.press(etat=False)

    def __eq__(self, other):
        if isinstance(other, Instruction_bouton):
            if self.type_bt == other.type_bt:
                self.get_bt()
                other.get_bt()
                return (self.bouton == other.bouton)
        return False
