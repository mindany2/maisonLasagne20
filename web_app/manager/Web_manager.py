from In_out.network.Client import Client
from tree.utils.Dico import Dico
from tree.utils.List_radio import List_radio
from In_out.network.messages.get.Get_states import Get_states

class Web_manager:
    """
    This class manage all the web site infos
    """
    def __init__(self):
        self.client = Client()
        self.list_pages = List_radio()

    def add_page(self, page):
        self.list_pages.add(page)

    def start(self):
        self.client.start()

    def get_active_page(self):
        return self.list_pages.selected()

    def get_page(self, name):
        return self.list_pages.get(name)

    def press_button(self, section, button):
        section = self.get_active_page().get_section(section)
        button = section.get_icon(button)
        button.press(self.client, "{}.{}.".format(self.get_active_page().name, section.name))

    def move_slider(self, section, slider, value):
        section = self.get_active_page().get_section(section)
        slider = section.get_icon(slider)
        slider.move(self.client, "{}.{}.".format(self.get_active_page().name, section.name), value)

    def pack(self):
        # setup the actual page
        print("request data")
        datas = self.client.send(Get_states())
        print(datas)
        # datas contains all the state of the icons
        for page in self.list_pages:
            for section in page.get_sections():
                for icon in section.get_list_icons():
                    try:
                        infos = datas["{}.{}.{}".format(page.name, section.name, icon.name)]
                        icon.change_state(True)
                        icon.change_infos(infos)
                    except KeyError as e:
                        icon.change_state(False)
                        print(e, icon)

        self.get_active_page().pack()



