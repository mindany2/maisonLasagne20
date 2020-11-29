from tree.scenario.instructions.Instruction import Instruction, STATE
from In_out.communication.PC import ACTIONS
from utils.communication.control.Press_key import Press_key
from utils.communication.control.Press_mouse import Press_mouse
from enum import Enum
from utils.Logger import Logger

class Instruction_PC(Instruction):
    """
    Allow to control an external personnal computer
    (if there are a serveur running at the startup of this PC
    """
    def __init__(self, calculator, pc, action, args, duration, delay, synchro):
        Instruction.__init__(self, calculator, duration, delay, synchro)
        self.pc = pc
        self.action = action
        self.args = args

    def run(self, barrier):
        super().run()
        if self.action == ACTIONS.allumer:
            self.pc.connect()
            Logger.info("Power on {}".format(self.pc.nom))

        elif self.action == ACTIONS.eteindre:
            self.pc.deconnect()
            Logger.info("Power off {}".format(self.pc.nom))

        elif self.action == ACTIONS.key:
            self.pc.send(Press_key(self.args[0]))
            Logger.info("press "+self.args[0])

        elif self.action == ACTIONS.mouse:
            double_clic = False
            clic_right = False
            x, y = self.args[0:2]
            if len(self.args) > 2:
                double_clic = (self.args[3] == "double")
                clic_right = (self.args[3] == "droit")
            self.pc.send(Press_mouse(x, y, clic_right, double_clic))
            Logger.info("clic "+self.args)




