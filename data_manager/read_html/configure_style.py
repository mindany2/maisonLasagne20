from web_app.buttons.style.Gradient import Gradient
from web_app.buttons.style.Style import Style
from copy import copy

LONGUEUR = 60

def config_style(line):
    """
    Setup the buttons styles 
    """
    list_color = line.colors[1].generate_array(line.colors[0], line.nb_buttons()+1)
    for i, bt in enumerate(line.get_buttons()):
        grad = Gradient(list_color[i],list_color[i+1])
        nb_caractère = len(bt.name)

        style = Style(size = (LONGUEUR,40),
                    background_image=grad,
                    margin = (-5, 0))

        bt.style_off = copy(style)
        bt.style_off.font_weight = "light"
        bt.style_off.font_size = 15

        bt.style_on = copy(style)
        bt.style_on.font_weight = "bolder"
        bt.style_on.font_size = 19

        if i == 0:
            # the first
            bt.style_off.set_border((True, False),(True, False))
            bt.style_on.set_border((True, False),(True, False))

        elif i == line.nb_buttons()-1:
            #the last
            bt.style_off.set_border((False, True),(False, True))
            bt.style_on.set_border((False, True),(False, True))

    line.set_style(Style(position= (0, line.nb_buttons()*LONGUEUR/2-len(line.name.split(".")[0])*4),
                    font_size = 18,
                    font_color = "black",
                    font_weight = "bolder"))
