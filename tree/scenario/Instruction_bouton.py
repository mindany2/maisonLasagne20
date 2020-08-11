from tree.scenario.Instruction import Instruction
from tree.boutons.Bouton_deco import Bouton_deco
from tree.Tree import Tree
from utils.Logger import Logger

class Instruction_bouton(Instruction):
    """
    Une instruction appellant un bouton d'un autre environnement
    """
    def __init__(self, nom_env, nom_preset, nom_scenar, etat, type_bt, temps_init, synchro):
        Instruction.__init__(self, 0, temps_init, synchro)
        self.nom_env = nom_env
        self.nom_preset = nom_preset
        self.nom_scenar = nom_scenar
        self.type_bt = type_bt
        self.etat = etat

        self.bouton = None
        self.preset = None
        self.env = None

    def run(self, temps_ecouler=0):
        super().run()

        if self.bouton == None:
            self.get_bt()

        if(self.env.get_preset_select() == self.preset):
            self.preset.change_select(self.bouton.press(self.etat))


    def get_bt(self):
        try:
            self.env = Tree.get_env(self.nom_env) 
            self.preset = self.env.get_preset(self.nom_preset)
            self.scenar = self.preset.get_scenar(self.nom_scenar)
            assert(self.scenar)

        except:
            raise(Exception("Not found exection scenar {} env {} preset {} n'existe pas"
                .format(self.nom_env, self.nom_env, self.nom_preset)))

        if self.type_bt == "deco":
            self.bouton = Bouton_deco(self.nom_env + "."+ self.nom_preset +"." + self.nom_scenar, self.env, self.scenar)

        else:
            raise(Exception("Type non pris en charge"))

            


    def __eq__(self, other):
        if isinstance(other, Instruction_bouton):
            return (self.bouton == other.bouton) and self.etat == other.etat

        return False
