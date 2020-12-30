from In_out.network.Client import Client
from tree.utils.Dico import Dico
from tree.utils.List_radio import List_radio

class Web_manager:
    """
    This class manage all the web site infos
    """
    def __init__(self):
        self.client = Client()

        self.list_pages = List_radio()
        self.list_modes = Dico()

    def add_page(self, page):
        self.list_pages.add(page)

    def add_mode(self, name_mode, page):
        self.list_modes.add(name_mode, page)

    def get_active_page(self):
        return self.list_pages.selected()

    def press_button(self, section, button):
        print(section, button)
        button = self.get_active_page().get_section(section).get_button(button)
        button.press()

    def pack(self):
        # setup the actual page
        self.get_active_page().pack()



