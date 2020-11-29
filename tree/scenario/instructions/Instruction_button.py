from tree.scenario.instructions.Instruction import Instruction
from tree.buttons.Button_secondary import Button_secondary
from tree.buttons.Button_principal import Button_principal
from tree.Tree import Tree
from utils.Logger import Logger
from enum import Enum

class TYPE_BUTTON(Enum):
    principal = 0
    secondary = 1

class Instruction_button(Instruction):
    """
    The instruction call a button for another environnement
    """
    def __init__(self,calculator, name_env, name_preset, list_name_scenars, type_bt, delay, synchro, condition):
        Instruction.__init__(self,calculator, 0, delay, synchro)
        self.name_env = name_env
        self.name_preset = name_preset
        self.name_scenars = list_name_scenars
        self.type_bt = type_bt
        self.condition = condition

        self.button = None
        self.preset = None
        self.env = None

    def run(self, barrier = None):
        super().run()
        self.get_bt()

        condition = self.eval(self.condition)
        # check if it is the right preset, if not just pass
        if(self.env.get_preset_select() == self.preset):
            # if there are only one scenario, just do it if the condition is True
            if len(self.name_scenars) == 1 and condition:
                self.button.press()
            elif len(self.name_scenars) > 1:
                # if not, just press the button with the condition like state
                # it is necessary a principal button
                self.button.press(state=condition)

    def get_bt(self):
        """
        Need to find the button after all the tree is created
        """
        if self.button:
            return
        try:
            # get the scenarios
            self.env = Tree.get_env(self.name_env) 
            self.preset = self.env.get_preset(self.name_preset)
            self.scenars = [self.preset.get_scenar(name_scenar) for name_scenar in self.name_scenars]
            for scenar in self.scenars:
                assert(scenar)

        except:
            raise(Exception("Not found exeption scenario : {}, in the environnement {}, preset : {}"
                .format(self.name_scenars, self.name_env, self.name_preset)))

        if self.type_bt == TYPE_BUTTON.principal:
            scenar_off = None
            if (len(self.scenars) > 1):
                scenar_off = self.scenars[1]
            self.button = Button_principal(self.name_env + "."+ self.name_preset +"." + self.name_scenars[0], self.env, self.scenars[0], scenar_off)
        elif self.type_bt == TYPE_BUTTON.secondary:
            self.button = Button_secondary(self.name_env + "."+ self.name_preset +"." + self.name_scenars[0], self.env, self.scenars[0])
        else:
            raise(Exception("Error type button : {}".format(self.type_bt)))

    def finish(self):
        if self.type_bt == TYPE_BUTTON.secondary:
            self.button.press(state=False)

    def __eq__(self, other):
        if isinstance(other, Instruction_button):
            if self.type_bt == other.type_bt:
                self.get_bt()
                other.get_bt()
                return (self.button == other.button)
        return False
