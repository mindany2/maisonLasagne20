from tree.scenario.instructions.Instruction import Instruction
from tree.buttons.Button_principal import Button_principal
from tree.buttons.Button_secondary import Button_secondary

from tree.utils.Logger import Logger
from enum import Enum

class TYPE_BUTTON(Enum):
    principal = 0
    secondary = 1

class Instruction_button(Instruction):
    """
    The instruction call a button for another environnement
    """
    def __init__(self, calculator, name_scenars, type_bt, delay, synchro, condition):
        Instruction.__init__(self,calculator, 0, delay, synchro)
        self.name_scenars = name_scenars
        self.type_bt = type_bt
        self.condition = condition

        self.button = None

    def run(self, barrier = None):
        super().run()

        if not(self.button):
            raise(Exception("Need to initialize the instruction before start"))

        condition = self.eval(self.condition)
        env, preset, scenars = self.name_scenars.get_scenarios(get_all = True)
        # check if it is the right preset, if not just pass
        if(env.get_preset_select() == preset):
            # if there are only one scenario, just do it if the condition is True
            if len(scenars) == 1 and condition:
                self.button.press()
            elif len(scenars) > 1:
                # if not, just press the button with the condition like state
                # it is necessary a principal button
                self.button.press(state=condition)

    def initialize(self):
        """
        Need to find the button after all the tree is created
        """
        super().initialize()
        self.eval(self.condition)

        env, preset, scenars = self.name_scenars.get_scenarios(get_all = True)

        if self.type_bt == TYPE_BUTTON.principal:
            scenar_off = None
            if (len(scenars) > 1):
                scenar_off = scenars[1]
            self.button = Button_principal("{}.{}.{}".format(env.name, preset.name, scenars[0].name),
                                preset.get_manager(), scenars[0], scenar_off)
        elif self.type_bt == TYPE_BUTTON.secondary:
            self.button = Button_secondary("{}.{}.{}".format(env.name, preset.name, scenars[0].name),
                                preset.get_manager(), scenars[0])
        else:
            self.condition.raise_error("Error type button : {}".format(self.type_bt))

    def finish(self):
        if self.type_bt == TYPE_BUTTON.secondary:
            self.button.press(state=False)

    def __eq__(self, other):
        if isinstance(other, Instruction_button):
            if self.type_bt == other.type_bt:
                return (self.button == other.button)
        return False

    def __str__(self):
        string = "".join("- Type : Bouton\n")
        string += super().__str__()
        return string
