from tree.scenario.instructions.Instruction import Instruction, STATE
from In_out.network.PC import ACTIONS
from In_out.network.messages.control.Press_key import Press_key
from In_out.network.messages.control.Press_mouse import Press_mouse
from enum import Enum
from tree.utils.Logger import Logger
from time import sleep

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
        self.pc.lock()
        if self.action == ACTIONS.power_on:
            self.pc.connect()
            Logger.info("Power on {}".format(self.pc.name))

        elif self.action == ACTIONS.power_off:
            self.pc.power_off()
            Logger.info("Power off {}".format(self.pc.name))

        elif self.action == ACTIONS.keys:
            self.pc.send(Press_key(self.args))
            sleep(0.1) # time to let the key 
            Logger.info("press "+str(self.args))

        elif self.action == ACTIONS.mouse:
            double_clic = False
            clic_right = False
            x, y = self.args[0:2]
            if len(self.args) > 2:
                double_clic = (self.args[3] == "double")
                clic_right = (self.args[3] == "droit")
            self.pc.send(Press_mouse(x, y, clic_right, double_clic))
            Logger.info("clic "+self.args)
        self.pc.unlock()

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : PC\n")
        string += "".join("- Action : {}\n".format(self.action))
        string += "".join("- Args : {}\n".format(self.args))
        return string



