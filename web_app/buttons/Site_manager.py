from tree.utils.List import List
from tree.utils.List_radio import List_radio
from In_out.network.Client import Client
from In_out.network.messages.get.Get_states import Get_states
from In_out.network.messages.interrupt.Press_inter import Press_inter
from In_out.network.messages.interrupt.Change_mode import Change_mode
from data_manager.read_html.configure_style import config_style

class Site_manager:
    """
    Store all site infos, lines and buttons
    """
    def __init__(self):
        self.lines = List()
        self.modes = List_radio()
        self.client = Client()

    def add_mode(self, mode):
        self.modes.add(mode)

    def get_current_mode(self):
        return self.modes.selected()

    def add_line(self, line):
        self.lines.add(line)

    def get_line(self, name):
        return self.lines.get(name)

    def build(self):
        # setup all the styles
        for line in self.lines:
            config_style(line)

        # and run the client
        self.client.start()
        self.reload()
        
    def reload(self):
        all_states = self.client.send(Get_states())
        name_mode = all_states["mode"]
        if name_mode != self.get_current_mode().name:
            self.modes.change_select(self.modes.get(name_mode))

        for line in self.lines:
            if line.get_link() in all_states.keys():
                for button in line.get_buttons():
                    button.change_state(button.name in all_states[line.get_link()])
                line.change_state(True)
            else:
                line.change_state(False)

    def get_lines(self):
        return [line for line in self.lines if line.state]

    def press_button(self, line, button):
        if line == "mode":
            self.modes.next()
            self.client.send(Change_mode(self.get_current_mode().name))
        else:
            line = self.lines.get(line)
            button = line.get_button(button)
            self.client.send(Press_inter(line.env_name, button.name, not(button.state)))
        self.reload()


    def __str__(self):
        string  = "-"*10 + "Site manager" + "-"*10 +"\n"
        string += "-Lines\n"
        string += "".join("|  {}\n".format(string) for string in str(self.lines).split("\n"))
        return string
