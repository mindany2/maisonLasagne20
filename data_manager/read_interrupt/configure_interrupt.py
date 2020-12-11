from data_manager.utils.File_yaml import File_yaml
from data_manager.utils.Csv_reader import Csv_reader
from data_manager.utils.file_manager import list_folders

from In_out.interrupts.inter import Interrupt_GPIO, Interrupt_cron, Interrupt_extender

PATH = "data/environnements"

def config_interrupt(getter):
    # go to each environnement and find every define interrupt
    # and store it in the getter

    get_interrupt(getter, PATH)

    print(getter)

def get_interrupt(getter, path):
    for sub_env in list_folders(path):
        if sub_env != "presets":
            get_interrupt(getter, path+"/"+sub_env)

    file = File_yaml(getter, path+"/config.yaml")
    interrupts = file.get("Interrupts")
    if interrupts:
        interrupts.get("config", mandatory = True, method=get_inter)

def get_inter(config):
    getter = config.get_getter()
    for inter in Csv_reader(getter,config):
        name, type_int, args = inter.get_str("name", mandatory=True), inter.get("type", mandatory=True), inter.get("args", mandatory=True)
        if str(type_int) == "extender":
            pin = int(args)
            getter.add_interrupt_extender(Interrupt_extender(name, pin, getter.get_client()))
        elif str(type_int) == "gpio":
            pin = int(args)
            getter.add_interrupt(Interrupt_GPIO(name, pin, getter.get_client()))
        elif str(type_int) == "cron":
            getter.add_interrupt(Interrupt_cron(name, args, getter.get_client()))
        else:
            type_int.raise_error("Type inter {} not found".format(str(type_int)))


