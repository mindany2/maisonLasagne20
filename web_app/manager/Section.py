from tree.utils.List import List
from web_app.manager.utils.Style import Style
from web_app.manager.icons.Icon_title import Icon_title

class Section:
    """
    This is an html section
    """
    def __init__(self, name, index=100, title = None, lenght = 3, background_color = "", text_color= ""):
        self.name = name
        self.title = None
        self.index = index
        if title:
            self.title = Icon_title(name, title, index=0, lenght=lenght, color=text_color)
        self.list_icons = List()
        self.background_color = background_color
        self.lenght = lenght
        self.style = None

    def add_icon(self, icon):
        self.list_icons.add(icon)

    def get_icon(self, name):
        return self.list_icons.get(name)

    def get_index(self):
        return self.index

    def pack(self, i):
        self.style = Style(display = "grid",
                           grid_templates_columns = "repeat(auto-fill, {}%)".format(int(100/self.lenght)),
                           grid = True, position = (i, 0),
                           align_items = "center",
                           background_color = self.background_color)
        decal = 0
        if self.title:
            self.title.pack(0,0)
            decal += self.lenght
        # decalage due to icon size
        for icon in sorted(list(self.list_icons), key = lambda x : x.get_index()):
            if icon.get_state():
                if icon.get_lenght() > decal%(self.lenght-1)+1:
                    decal += self.lenght-(decal%self.lenght)
                icon.pack(decal//self.lenght, decal%self.lenght)
                decal += icon.get_lenght()

    def get_style(self):
        return self.style

    def get_icons(self):
        return list(self.list_icons)+[self.title]




