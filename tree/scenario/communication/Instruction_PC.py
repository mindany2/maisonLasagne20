from tree.scenario.Instruction import Instruction, Attente
from tree.eclairage.Lumiere import Lumiere
from In_out.communication.PC import ACTIONS
from utils.communication.control.Press_key import Press_key
from utils.communication.control.Press_mouse import Press_mouse
from enum import Enum

class Instruction_PC(Instruction):
    """
    Pertmet de commander un PC
    """
    def __init__(self, pc, action, args, duree, temps_init, synchro):
        Instruction.__init__(self, duree, temps_init, synchro)
        self.pc = pc
        self.action = action
        self.args = args

    def run(self, barrier):
        super().run()
        if self.action == ACTIONS.allumer:
            self.pc.connect()

        elif self.action == ACTIONS.eteindre:
            self.pc.deconnect()

        elif self.action == ACTIONS.key:
            self.pc.send(Press_key(self.args))

        elif self.action == ACTIONS.mouse:
            args = args.split(",")
            double_clic = False
            clic_right = False
            x, y = args[0:2]
            if len(args) > 2:
                double_clic = (args[3] == "double")
                clic_right = (args[3] == "droit")
            self.pc.send(Press_mouse(x, y, clic_right, double_clic))




