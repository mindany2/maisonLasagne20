from data_manager.utils.Reader import Reader
import ruamel.yaml

class File_yaml(Reader):
    """
    Read a yaml file
    """
    def __init__(self, path):
        with open(path, "r") as config_file:
            Reader.__init__(self, ruamel.yaml.load(config_file, Loader=ruamel.yaml.RoundTripLoader), path)


