from tree.buttons.Button import Button
from tree.scenario.Scenario import MARKER

class Button_choice(Button):
    """
    Button with a list of scenarios, switch to one another in order
    """
    def __init__(self, name, manager, list_scenar):
        Button.__init__(self, name, manager)
        self.list_scenar = list_scenar

    def press(self, state= None):
        select = 0
        for i,scenar in enumerate(self.list_scenar):
            if self.manager.get_scenar_en_cours() == scenar:
                select = i+1
                if select == len(self.list_scenar):
                    select = 0
                break
        scenar = self.list_scenar[select]
        self.manager.do_scenar_principal(scenar)

    def __str__(self):
        string = super().__str__()
        string += "- Type : choice\n"
        string += "- Scenarios\n"
        string += "".join(["|-{}\n".format(scenar.name) for scenar in self.list_scenar])
        return string




