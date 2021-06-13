from tree.utils.calculs.Variable import Variable

class Variable_spotify(Variable):
    """
    Get spotify variables
    """
    def __init__(self, spotify):
        self.spotify = spotify
        Variable.__init__(self, "spotify", 0)

    def get(self, inst, variable_name):
        if variable_name.count("bpm") == 1:
            return self.spotify.get_bpm()
        elif variable_name.count("volume") == 1:
            return self.spotify.get_volume()
        elif variable_name.count("state") == 1:
            return self.spotify.get_state()
        raise(NameError("The variable {} in spotify doesn't existe".format(variable_name)))

    def reload(self, other):
        pass

    def set(self, val):
        raise(ReferenceError("Cannot set an this variable"))
