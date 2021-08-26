from data_manager.utils.File_yaml import File_yaml
from data_manager.utils.Csv_reader import Csv_reader
from data_manager.utils.file_manager import list_folders

from In_out.interrupts.inter import Interrupt_GPIO, Interrupt_cron, Interrupt_extender, Interrupt
from In_out.zigbee.devices.Zigbee_contact import Zigbee_contact
from In_out.zigbee.devices.Zigbee_ir_sensor import Zigbee_ir_sensor
from In_out.zigbee.devices.Zigbee_hum_temp_sensor import Zigbee_hum_temp_sensor

PATH = "data/environnements"

def config_interrupt(getter):
    # go to each environnement and find every define interrupt
    # and store it in the getter

    get_interrupt(getter, PATH, "global")

    print(getter)

def get_interrupt(getter, path, name_env):
    for sub_env in list_folders(path):
        if sub_env != "presets":
            get_interrupt(getter, path+"/"+sub_env, name_env+"."+sub_env)

    file = File_yaml(getter, path+"/config.yaml")
    interrupts = file.get("Interrupts")
    if interrupts:
        interrupts.get("config", mandatory = True, method=get_inter, args=name_env)

def get_inter(config, name_env):
    getter = config.get_getter()
    for inter in Csv_reader(getter,config):
        name, type_int, args = inter.get_str("name", mandatory=True), inter.get("type", mandatory=True), inter.get("args", mandatory=True)
        if str(type_int) == "extender":
            pin = int(args)
            getter.add_interrupt_extender(Interrupt_extender(name, name_env, pin, getter.get_client()))
        elif str(type_int) == "gpio":
            pin = int(args)
            getter.add_interrupt(Interrupt_GPIO(name, name_env, pin, getter.get_client()))
        elif str(type_int) == "cron":
            getter.add_interrupt(Interrupt_cron(name, name_env, args, getter.get_client()))
        elif str(type_int) == "zigbee":
            zigbee = getter.get_zigbee()
            if not zigbee:
                type_int.raise_error("No zigbee module")
            sub_type = inter.get_str("sub_type", mandatory=True)

            try:
                addr = zigbee.get_device(str(args))
            except KeyError:
                type_int.raise_error(f"Could not find the {args} device. \n {zigbee}")

            if sub_type == "contact":
                device = Zigbee_contact(name, addr, Interrupt(name, name_env, getter.get_client()))
            elif sub_type == "ir_sensor":
                device = Zigbee_ir_sensor(name, addr, Interrupt(name, name_env, getter.get_client()))

            elif sub_type == "temp&hum":
                device = Zigbee_hum_temp_sensor(name, addr, Interrupt(name, name_env, getter.get_client()))
            else:
                type_int.raise_error(f"Unknown sub-type {sub_type}")

            zigbee.add_device(device)



        elif str(type_int) != "network":
            type_int.raise_error("Type inter {} not found".format(str(type_int)))



