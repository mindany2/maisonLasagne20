from data_manager.utils.Csv_reader import Csv_reader

from tree.connected_objects import Led, Dimmable_light, Lamp, Speakers, Trap
from tree.connected_objects.dmx import Dmx_dimmable_light, Lyre, Crazy_2, Galaxy_laser, Strombo

from tree.scenario.instructions.utils.Delay import Delay
from tree.scenario.instructions import Instruction_button, TYPE_BUTTON, Instruction_trap, TYPE_INST_TRAP
from tree.scenario.instructions import Instruction_spotify, TYPE_INST_SPOTIFY, Instruction_variable, Instruction_interrupt
from tree.scenario.instructions import Instruction_mode, Instruction_speaker
from tree.scenario.instructions.light import Instruction_color, Instruction_dimmer, Instruction_force, Instruction_power
from tree.scenario.instructions.light.dmx import Instruction_color_wheel, Instruction_gobo, Instruction_position, Instruction_program
from tree.scenario.instructions.light.dmx import Instruction_speed, Instruction_strombo
from tree.scenario.instructions.Instruction_PC import Instruction_PC, ACTIONS

from tree.connected_objects import Led, Dimmable_light, Lamp, Speakers, Trap, BULD
from tree.connected_objects.dmx import Dmx_dimmable_light, Lyre, Crazy_2, Galaxy_laser, Strombo, Dmx_strip_led
from tree.utils.calculs.Variable import Variable 
from In_out.network.Rpi import Rpi
from In_out.network.PC import PC

import re

def get_instructions(list_inst, args):
    env, scenar = args
    getter = list_inst.get_getter()
    instructions = Csv_reader(getter, list_inst)
    for inst in instructions:
        name, delay_value, duration = inst.get("name", mandatory=True), inst.get("delay", mandatory=True), inst.get("duration")
        args, type_inst = inst.get("args"), inst.get("type", mandatory = True)
        # Type
        try:
            type_inst = TYPE[str(type_inst)]
        except KeyError:
            type_inst.raise_error("The instruction type {} does not exist, this is the allowed keys :\n {}"
                            .format(str(type_inst), [str(arg) for arg in TYPE]))
        #Synchro
        synchro = (delay_value == "synchro")
        if synchro: delay = "0"

        #Delay
        wait_for_beat = delay_value.get_wait_for_beat()
        wait_precedent = delay_value.get_wait_precedent()
        delay = Delay(getter.get_manager(), env.get_calculator(), delay_value, wait_for_beat, wait_precedent)

        scenar.add_inst(type_inst(env, name, delay, duration, args, synchro))

def get_inst_strombo(env, name, delay, duration, args, synchro):
    light = name.get_object(env, (Lyre, Strombo, Crazy_2))
    return Instruction_gobo(env.get_calculator(), light, args, duration, delay, synchro)

def get_inst_speed(env, name, delay, duration, args, synchro):
    light = name.get_object(env, (Lyre, Crazy_2))
    return Instruction_speed(env.get_calculator(), light, args, duration, delay, synchro)

def get_inst_program(env, name, delay, duration, args, synchro):
    light = name.get_object(env, Crazy_2)
    return Instruction_program(env.get_calculator(), light, args, duration, delay, synchro)

def get_inst_position(env, name, delay, duration, args, synchro):
    light = name.get_object(env, Lyre)
    pan, tilt = args.split(",")
    return Instruction_position(env.get_calculator(), light, pan, tilt, duration, delay, synchro)

def get_inst_gobo(env, name, delay, duration, args, synchro):
    light = name.get_object(env, Lyre)
    return Instruction_gobo(env.get_calculator(), light, args, duration, delay, synchro)

def get_inst_color_wheel(env, name, delay, duration, args, synchro):
    light = name.get_object(env, Lyre)
    return Instruction_color_wheel(env.get_calculator(), light, args, duration, delay, synchro)

def get_inst_speaker(env, name, delay, duration, args, synchro):
    speaker = name.get_object(env, Speakers)
    return Instruction_speaker(env.get_calculator(), speaker, args, duration, delay, synchro)

def get_inst_power(env, name, delay, duration, args, synchro):
    light = name.get_object(env, (Lamp, Speakers))
    return Instruction_power(env.get_calculator(), light, args, duration, delay, synchro)

def get_inst_amp(env, name, delay, duration, args, synchro):
    amp = name.get_amp()
    return Instruction_power(env.get_calculator(), amp, args, duration, delay, synchro)

def get_inst_force(env, name, delay, duration, args, synchro):
    light = name.get_object(env, Lamp)
    return Instruction_force(env.get_calculator(), light, args, duration, delay, synchro)

def get_inst_dimmer(env, name, delay, duration, args, synchro):
    light = name.get_object(env, (Dimmable_light, Dmx_dimmable_light, Lyre, Strombo))
    return Instruction_dimmer(env.get_calculator(), light, args, duration, delay, synchro)

def get_inst_color(env, name, delay, duration, args, synchro):
    dimmer, color = args.split(",", 2)
    light = name.get_object(env, (Led, Dmx_strip_led))
    return Instruction_color(env.get_calculator(), light, dimmer, duration, delay, synchro, color)

def get_inst_pc(env, name, delay, duration, args, synchro):
    match = re.match(r'(?P<action>([^\(]*))\((?P<args>([^\)]*))\)', str(args))
    if not(match):
        args.raise_error("Could not match the action, try this syntax : mouse(200,300) or key(space)")
    try:
        action = ACTIONS[match.group("action")]
        args = match.group("args").replace(" ","").split(",")
    except KeyError:
        args.raise_error("PC action {} not define this is the allowed keys :\n {}".
                        format(str(args), [arg.name for arg in ACTIONS]))
    try:
        pc = name.get_getter().get_manager().get_connection(str(name))
        assert(isinstance(pc, PC))
    except NameError as e:
        name.raise_error(str(e))
    except AssertionError:
        name.raise_error("The instruction pc is only available for {}".format(PC))
    return Instruction_PC(env.get_calculator(), pc, action, args, duration, delay, synchro)

def get_inst_variable(env, name, delay, duration, args, synchro):
    try:
        variable = name.get_getter().get_var(env, str(name))
        assert(isinstance(variable, Variable))
    except (NameError, KeyError) as e:
        name.raise_error(str(e))
    except AssertionError:
        name.raise_error("The instruction variable is only available for {}".format(Variable))
    return Instruction_variable(env.get_calculator(), variable, args, duration, delay, synchro)

def get_inst_trap(env, name, delay, duration, args, synchro):
    try:
        type_inst = TYPE_INST_TRAP[str(args)]
    except KeyError:
        args.raise_error("Trap action {} not define this is the allowed keys :\n {}".
                        format(str(args), [arg.name for arg in TYPE_INST_TRAP]))
    try:
        trap = get_object(env, str(name))
        assert(isinstance(trap, Trap))
    except NameError as e:
        name.raise_error(str(e))
    except AssertionError:
        name.raise_error("The instruction trap is only available for {}".format(Trap))
    return Instruction_trap(env.get_calculator(), trap, type_inst, duration, delay, synchro)

def get_inst_spotify(env, name, delay, duration, args, synchro):
    try:
        try:
            type_inst, arg = args.split(",")
            type_inst = TYPE_INST_SPOTIFY[str(type_inst)]
            if type_inst in [TYPE_INST_SPOTIFY.volume, TYPE_INST_SPOTIFY.start_playlist]:
                val = arg
            else:
                args.raise_error("Spotify action volume, playlist need to have an argument like : volume, 50")
        except ValueError:
            type_inst = TYPE_INST_SPOTIFY[str(args)]
            val = 0
    except KeyError:
        args.raise_error("Spotify action {} not define this is the allowed keys :\n {}".
                        format(str(args), [arg.name for arg in TYPE_INST_SPOTIFY]))
    return Instruction_spotify(env.get_calculator(), name.get_spotify(), type_inst, val, delay, synchro)

def get_inst_interrupt(env, name, delay, duration, args, synchro):
    manager = name.get_getter().get_manager()
    try:
        conn = manager.get_connection(str(name))
    except NameError as e:
        name.raise_error(str(e))
    name_inter, state = args.split(",", 2)
    conn.add_output_interrupt(str(name_inter))
    return Instruction_interrupt(env.get_calculator(), conn, name_inter, state, delay, synchro)

def get_inst_button_sec(env, name, delay, duration, args, synchro):
    return Instruction_button(env.get_calculator(), name, TYPE_BUTTON.secondary, delay, args, synchro)

def get_inst_button_prin(env, name, delay, duration, args, synchro):
    return Instruction_button(env.get_calculator(), name, TYPE_BUTTON.principal, delay, args, synchro)

def get_inst_mode(env, name, delay, duration, args, synchro):
    tree = name.get_getter().get_tree()
    return Instruction_mode(env.get_calculator(), tree, str(name), delay, args, synchro)


TYPE = {"button_secondary" : get_inst_button_sec,
        "button_principal" : get_inst_button_prin,
        "spotify": get_inst_spotify,
        "interrupt": get_inst_interrupt,
        "trap" : get_inst_trap,
        "variable": get_inst_variable,
        "pc" : get_inst_pc,
        "amp": get_inst_amp,
        "color" : get_inst_color,
        "dimmer" : get_inst_dimmer,
        "force" : get_inst_force,
        "power" : get_inst_power,
        "speakers" : get_inst_speaker,
        "color_wheel" : get_inst_color_wheel,
        "gobo" : get_inst_gobo,
        "position" : get_inst_position,
        "program" : get_inst_program,
        "speed" : get_inst_speed,
        "strombo" : get_inst_strombo,
        "mode" : get_inst_mode}
