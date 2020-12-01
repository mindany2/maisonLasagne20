from tree.utils.calculs.Variable import Variable
from utils.spotify.Spotify import Spotify

class Variables_spotify(Variable):
    """
    Get spotify variables
    """
    def __init__(self):
        Variable.__init__(self, "spotify", 0)

    def get(self, variable_name):
        if variable_name.count("bpm") == 1:
            return Spotify().get_bpm()
        elif variable_name.count("volume") == 1:
            return Spotify().get_volume()
        elif variable_name.count("state") == 1:
            return Spotify().get_state()
        raise(Exception("The variable {} in spotify doesn't existe".format(variable_name)))

    def set(self, val):
        raise(Exception("Cannot set an this variable"))
        
