from data_manager.utils.Csv_reader import Csv_reader

from tree.connected_objects import Led, Dimmable_light, Lamp, Speakers, Trap, BULD
from tree.connected_objects.dmx import Dmx_dimmable_light, Lyre, Crazy_2, Galaxy_laser, Strombo, Dmx_strip_led

from In_out.bluetooth_devices import ELK_BLEDOM, LEDBLE, TRIONES
from In_out.wifi_devices import LEDnet
from In_out.sensors.Sensor_GPIO import Sensor_GPIO

from enum import Enum

def get_objects(objects, env):
    getter = objects.get_getter()
    objects = Csv_reader(getter, objects.get("config"))
    for obj in objects:
        name, sub_type, addr = obj.get_str("name", mandatory = True), obj.get("sub_type"), obj.get("addr")
        type_obj, relay_triak = obj.get("type", mandatory = True), obj.get_addr("relay/triak")
        try:
            method = TYPE[str(type_obj)]
        except KeyError:
            type_obj.raise_error("The type {} is does not exist".format(str(type_obj)))
        env.add_object(method(getter, name, sub_type, relay_triak, addr))

def get_dimmable(getter, name, sub_type, relay_triak, addr):
    if str(sub_type) == "dmx":
        if not(str(addr)):
            addr.raise_error("The {} need an dmx address".format(name))
        return Dmx_dimmable_light(name, relay_triak.get_relay(), int(addr), getter.get_dmx())
    try:
        buld = BULD[str(sub_type)]
    except KeyError:
        sub_type.raise_error("The sub_type {} is not present in the BULD (Dimmable_light.py)".format(str(sub_type)))
    return Dimmable_light(name, relay_triak.get_triak(), buld)

def get_led(getter, name, sub_type, relay_triak, addr):
    if not(str(addr)):
        addr.raise_error("The {} need an address".format(name))
    try:
        controller = TYPE_LED[str(sub_type)](str(addr))
    except KeyError:
        if str(sub_type) == "dmx":
            return Dmx_strip_led(name, relay_triak.get_relay(), int(addr), getter.get_dmx())
        sub_type.raise_error("The sub_type {} is not present in the TYPE_LED".format(str(sub_type)))
    return Led(name, relay_triak.get_relay(), controller)

def get_lamp(getter, name, sub_type, relay_triak, addr):
    return Lamp(name, relay_triak.get_relay())

def get_speakers(getter, name, sub_type, relay_triak, addr):
    index_channel = relay_triak.get_int("index", mandatory = True)
    name_amp = relay_triak.get_str("board", mandatory = True)
    amp = getter.get_amp(name_amp)
    zone = amp.get_channel(index_channel)
    return Speakers(name, amp, zone)

def get_trap(getter, name, sub_type, relay_triak, addr):
    #TODO
    trap = relay_triak.split(",", 4) 
    relay_up, relay_down, magnet, sensor_addr = trap.get_addr(0), trap.get_addr(1), trap.get_addr(2), trap.get_addr(3)
    sensor = None
    if sensor_addr[1] == "rpi":
        sensor = Sensor_GPIO("Trap_closed_sensor", int(sensor_addr[0]))
    return Trap("Trap", getter.get_relay(relay_up), getter.get_relay(relay_down), getter.get_relay(magnet), sensor)

def get_crazy(getter, name, sub_type, relay_triak, addr):
    if not(str(addr)):
        addr.raise_error("The {} need an dmx address".format(name))
    return Crazy_2(name, relay_triak.get_relay(), int(addr), getter.get_dmx())

def get_laser(getter, name, sub_type, relay_triak, addr):
    #TODO
    pass

def get_lyre(getter, name, sub_type, relay_triak, addr):
    if not(str(addr)):
        addr.raise_error("The {} need an dmx address".format(name))
    return Lyre(name, relay_triak.get_relay(), int(addr), getter.get_dmx())

def get_strombo(getter, name, sub_type, relay_triak, addr):
    if not(str(addr)):
        addr.raise_error("The {} need an dmx address".format(name))
    return Strombo(name, relay_triak.get_relay(), int(addr), getter.get_dmx())

        
TYPE_LED = { "lednet" : LEDnet,
             "bledom" : ELK_BLEDOM,
             "triones": TRIONES,
             "ledble" : LEDBLE}

TYPE = {"dimmable" : get_dimmable,
        "led" : get_led,
        "lamp" : get_lamp,
        "speakers" : get_speakers,
        "trap" : get_trap,
        "crazy_2" : get_crazy,
        "laser" : get_laser,
        "lyre" : get_lyre,
        "strombo" : get_strombo}

