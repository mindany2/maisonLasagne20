from tree.utils.List import List
from web_app.manager.utils.Style import Style

class Page:
    """
    This is an html complete page
    """
    def __init__(self, name, background_image = None, background_color=None):
        self.name = name
        self.background_color = background_color
        self.background_image = background_image
        self.list_sections = List()
        self.style = None
        self.state = False

    def change_state(self, state):
        self.state = state

    def add_section(self, section):
        self.list_sections.add(section)

    def get_sections(self):
        return self.list_sections

    def get_section(self, name):
        return self.list_sections.get(name)

    def get_style(self):
        return self.style

    def pack(self):
        self.style = Style(display = "grid", grid_templates_columns="repeat(auto-fill, 100%)",
                            align_items = "center", background_image = self.background_image,
                            background_color = self.background_color)
        for i,section in enumerate(sorted(list(self.list_sections), key = lambda x : x.get_index())):
            section.pack(i)


