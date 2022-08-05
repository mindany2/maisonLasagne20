from tree.scenario.instructions.Instruction import Instruction
from tree.utils.Logger import Logger

class Instruction_interrupt(Instruction):
    """
    Modifie spotify values like volumes, play/pause..
    """
    #TODO volume
    def __init__(self,calculator, connection, name, state, delay, synchro, duration = 0):
        Instruction.__init__(self,calculator, duration, delay, synchro)
        self.name = name
        self.state = state
        self.connection = connection

    def run(self, barrier=None):
        self.connection.lock()
        super().run()
        if not(self.connection.test()):
            self.connection.send_interrupt(str(self.name), self.eval(self.state))
        self.connection.unlock()

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : inter\n")
        string += "".join("- connection : {}\n".format(self.connection.name))
        string += "".join("- inter : {}\n".format(self.name))
        return string
