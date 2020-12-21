from tree.utils.calculs.Variable import Variable
from In_out.Peripheric_manager import Peripheric_manager

class Variable_spotify(Variable):
    """
    Get spotify variables
    """
    def __init__(self):
        Variable.__init__(self, "spotify", 0)

    def get(self, getter, variable_name):
        spotify = Peripheric_manager().get_spotify()
        if not(spotify):
            raise(ValueError("There are no spotify configured"))
        if variable_name.count("bpm") == 1:
            return spotify.get_bpm()
        elif variable_name.count("volume") == 1:
            return spotify.get_volume()
        elif variable_name.count("state") == 1:
            return spotify.get_state()
        raise(NameError("The variable {} in spotify doesn't existe".format(variable_name)))

    def set(self, val):
        raise(ReferenceError("Cannot set an this variable"))
        
    def __str__(self):
        return ""
