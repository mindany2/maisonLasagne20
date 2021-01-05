from data_manager.utils.File_yaml import File_yaml
from In_out.interrupts.List_interrupts_extender import List_interrupts_extender
from In_out.utils.Port_extender import Port_extender

def configure_boards(getter):
    """
    Read the config file in data
    to setup the Peripheric_manager
    """
    config = File_yaml(getter, "data/config.yaml")

    # BOARDS
    config.get("BOARDS", get_boards)


def get_boards(boards):
    extender = boards.get("Port_extender")
    if extender:
        extender.get("interrupts", get_inter)

def get_inter(list_interrupts):
    getter = list_interrupts.get_getter()
    port_extender = Port_extender()
    for interrupts in list_interrupts:
        addr, gpio = interrupts.get_int("addr", mandatory = True), interrupts.get_int("gpio_port", mandatory=True)
        register = interrupts.get_int("register", mandatory = True)
        getter.configure_list_extender(List_interrupts_extender(port_extender, gpio, addr, register))
