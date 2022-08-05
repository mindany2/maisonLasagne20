from In_out.network.messages.Message import Message

class Get_states(Message):

    def __init__(self):
        pass

    def do(self, getter):
        """
        return a dict with all the preset active and all there active buttons
        also with the mode selected
        """
        # get current mode buttons 
        all_states = {}
        for mode in getter.get_tree().get_modes():
            for inter in mode.get_inters():
                all_states[inter] =  {"value":mode.get_state()}
        list_envs = getter.get_tree().get_list_envs()
        for env in list_envs:
            for button in env.get_preset_select().get_buttons():
                all_states[button.name] = {"value":button.state()}
        # get also spotify states and images
        try:
            all_states.update(getter.get_spotify().get_states())
        except NameError:
            pass
        return all_states



