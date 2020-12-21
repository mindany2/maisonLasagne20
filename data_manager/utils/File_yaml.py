from data_manager.utils.Reader import Reader
import ruamel.yaml
import os

class File_yaml(Reader):
    """
    Read a yaml file
    """
    def __init__(self, getter, path):
        with open(path, "r") as config_file:
            Reader.__init__(self, getter, ruamel.yaml.load(config_file, Loader=ruamel.yaml.RoundTripLoader), path)


