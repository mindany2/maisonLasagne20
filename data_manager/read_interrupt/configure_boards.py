from data_manager.utils.File_yaml import File_yaml
from In_out.interrupts.List_interrupts_extender import List_interrupts_extender
from In_out.utils.Port_extender import Port_extender
from In_out.utils.Zigate import Zigate
from In_out.zigbee.Zigbee_manager import Zigbee_manager

def configure_boards(getter):
    """
    Read the config file in data
    to setup the Peripheric_manager
    """
    config = File_yaml(getter, "data/config.yaml")

    # BOARDS
    config.get("BOARDS", get_boards)

    #ZIGBEE
    config.get("ZIGBEE", get_zigbee)

def get_zigbee(zigbee):
    module = zigbee.get("module", mandatory=True)
    if str(module) == "zigate":
        choosen_module = Zigate
    else:
        module.raise_error("Only zigate module available")
    zigbee.get_getter().add_zigbee(Zigbee_manager(choosen_module))

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
