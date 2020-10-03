from tree.scenario.Instruction import Instruction
from tree.boutons.Bouton_deco import Bouton_deco
from tree.boutons.Bouton_poussoir import Bouton_poussoir
from tree.Tree import Tree
from utils.Logger import Logger
from enum import Enum

class TYPE_BOUTON(Enum):
    scenar = 0
    deco = 1
    poussoir = 2


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

    def run(self, barrier = None, etat=True):
        if etat:
            # on attend que si on doit le mettre
            # pas si on doit l'enlever
            super().run()

        if self.bouton == None:
            self.get_bt()

        if(self.env.get_preset_select() == self.preset):
            Logger.info("Environnement :  {}, etat = {}".format(self.nom_env, etat))
            if self.type_bt != TYPE_BOUTON.scenar and self.eval(self.condition):
                self.bouton.press(self.eval(etat))
            elif self.type_bt == TYPE_BOUTON.scenar:
                condition = self.eval(self.condition)
                if condition:
                    self.scenars[0].do()
                    self.scenars[0].set_etat(True)
                    if len(self.scenars) > 1:
                        self.scenars[1].set_etat(False)
                elif len(self.scenars) > 1:
                    self.scenars[1].do()
                    self.scenars[1].set_etat(True)
                    self.scenars[0].set_etat(False)

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

        if self.type_bt == TYPE_BOUTON.deco:
            self.bouton = Bouton_deco(self.nom_env + "."+ self.nom_preset +"." + self.nom_scenars[0], self.env, self.scenars[0])
        elif self.type_bt == TYPE_BOUTON.poussoir:
            self.bouton = Bouton_poussoir(self.nom_env + "."+ self.nom_preset +"." + self.nom_scenars[0], self.env, self.scenars[0])
        elif self.type_bt == TYPE_BOUTON.scenar:
            self.bouton = 1

    def finish(self):
        if self.type_bt == TYPE_BOUTON.deco:
            self.run(etat = False)

    def __eq__(self, other):
        if isinstance(other, Instruction_bouton):
            if self.type_bt == other.type_bt:
                if self.type_bt != TYPE_BOUTON.scenar:
                    return (self.bouton == other.bouton)
                else:
                    return self.scenars[0] == other.scenars[0]
        return False
