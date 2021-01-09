from tree.utils.List import List
from web_app.manager.utils.Style import Style
from web_app.manager.icons.Icon_title import Icon_title

class Section:
    """
    This is an html section
    """
    def __init__(self, name, index=None, title = None, lenght = None, background_color = "", text_color= ""):
        self.index = 100 if index is None else index
        self.lenght = 100 if lenght is None else lenght
        self.name = name
        self.title = None
        if title:
            print("ooooooooooooooooooo")
            print(title, type(title))
            self.title = Icon_title(name, title, index=0, lenght=lenght, color=text_color)
        self.list_icons = List()
        self.background_color = background_color
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
        print(self.list_icons)
        for icon in sorted(list(self.list_icons), key = lambda x : x.get_index()):
            if icon.get_state():
                if icon.get_lenght() > decal%(self.lenght-1)+1:
                    decal += self.lenght-(decal%self.lenght)
                icon.pack(decal//self.lenght, decal%self.lenght)
                decal += icon.get_lenght()

    def get_style(self):
        return self.style

    def get_list_icons(self):
        return self.list_icons

    def get_icons(self):
        list_active = [icon for icon in self.list_icons if icon.get_state()]
        if list_active:
            if self.title:
                list_active += [self.title]
                print(self.title)
            return list_active
        return []




