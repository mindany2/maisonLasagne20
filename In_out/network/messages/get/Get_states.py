from In_out.network.messages.Message import Message

class Get_states(Message):

    def __init__(self):
        pass

    def do(self, getter):
        """
        return a dict with all the preset active and all there active buttons
        also with the mode selected
        """
        active_preset = {"mode": getter.get_tree().get_current_mode().name}
        list_envs = getter.get_tree().get_list_envs()
        for name_env in list_envs.keys():
            preset = list_envs.get(name_env).get_preset_select()
            list_active_buttons = [button.name for button in preset.get_buttons() if button.state()]
            active_preset[name_env+"."+preset.name] = list_active_buttons
        return active_preset



