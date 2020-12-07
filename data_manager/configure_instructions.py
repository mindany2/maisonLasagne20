from data_manager.utils.Csv_reader import Csv_reader

from tree.connected_objects import Led, Dimmable_light, Lamp, Speakers, Trap
from tree.connected_objects.dmx import Dmx_dimmable_light, Lyre, Crazy_2, Galaxy_laser, Strombo

from tree.scenario.instructions.utils.Delay import Delay
from tree.scenario.instructions import Instruction_button, TYPE_BUTTON, Instruction_trap, TYPE_INST_TRAP
from tree.scenario.instructions import Instruction_spotify, TYPE_INST_SPOTIFY, Instruction_variable, TYPE_INST_VAR
from tree.scenario.instructions.light import Instruction_color, Instruction_dimmer, Instruction_force, Instruction_lamp, Instruction_speaker
from tree.scenario.instructions.light.dmx import Instruction_color_wheel, Instruction_gobo, Instruction_position, Instruction_program
from tree.scenario.instructions.light.dmx import Instruction_speed, Instruction_strombo
from tree.scenario.instructions.communication.Instruction_PC import Instruction_PC

import re

def get_instructions(list_inst, args):
    env, scenar = args
    instructions = Csv_reader(list_inst)
    for inst in instructions:
        name, delay, duration = inst.get("name", mandatory=True), inst.get_str("delay", mandatory=True), inst.get_str("duration")
        args, type_inst = inst.get("args"), inst.get("type", mandatory = True)
        # Type
        try:
            type_inst = TYPE[str(type_inst)]
        except KeyError:
            type_inst.raise_error("The instruction type {} does not exist try the following :\n {}"
                            .format(str(type_inst), [arg.name for arg in TYPE]))
        #Synchro
        synchro = (delay == "synchro")
        if synchro: delay = "0"

        #Delay
        match = re.match(r'bpm_(?P<number>([0-9]*))[ ]*\+[ ]*(?P<delay>(.)*)', str(delay))
        wait_for_beat = 0
        if match:
            # bpm delay
            wait_for_beat, delay = int(match.group("number")), match.group("delay")
        delay = Delay(delay, wait_for_beat)

        scenar.add_inst(type_inst(env, name, delay, duration, args, synchro))

def get_inst_spotify(env, name, delay, duration, args, synchro):
    try:
        type_inst = TYPE_INST_SPOTIFY[str(args)]
    except KeyError:
        args.raise_error("Spotify action {} not define try the following :\n {}".format(str(args), [arg.name for arg in TYPE_INST_SPOTIFY]))
    return Instruction_spotify(

def get_inst_button_sec(env, name, delay, duration, args, synchro):
    return get_inst_button(env, name, delay, duration, args, synchro, TYPE_BUTTON.secondary)

def get_inst_button_prin(env, name, delay, duration, synchro, args):
    return get_inst_button(env, name, delay, duration, args, synchro, TYPE_BUTTON.principal)

def get_inst_button(env, name, delay, duration, args, synchro, type_bt):
    # Cut the name like 
    # env1.env2.preset.scenar1, scenar2
    match = re.match(r'(?P<env>([\w\.]*))\.(?P<preset>([^\.]*))\.(?P<scenar1>([^\,]*))', str(name))
    if match:
        name_env, name_preset, name_scenars = match.group("env"), match.group("preset"), [match.group("scenar1")]
    else:
        name.raise_error("Could not found a scenario like : env1.env2.preset1.scenar1, scenar2")
    match = re.match(r'[^\,]*\,[ ]*(?P<scenar2>([\w\.]*))', str(name))
    if match:
        if type_bt == TYPE_BUTTON.secondary:
            name.raise_error("A secondary button cannot have more than one scenario")
        name_scenars.append(match.group("scenar2"))
    return Instruction_button(env.get_calculator(), name_env, name_preset, name_scenars, type_bt, delay, synchro, args)


TYPE = {"secondary_button" : get_inst_button_sec,
        "principal_button" : get_inst_button_prin,
        "spotify": get_inst_spotify,
        "trap" : get_inst_trap,
        "variable": get_inst_variable,
        "pc" : get_inst_PC,
        "color" : get_inst_color,
        "dimmer" : get_inst_dimmer,
        "force" : get_inst_force,
        "lamp" : get_inst_lamp,
        "speaker" : get_inst_speaker,
        "color_wheel" : get_inst_color_wheel,
        "gobo" : get_inst_gobo,
        "position" : get_inst_position,
        "program" : get_inst_program,
        "speed" : get_inst_speed,
        "strombo" : get_inst_strombo}

