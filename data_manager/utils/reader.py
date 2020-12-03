import yaml

def read_yaml(path):
    """
    Read a yaml file
    """
    config_file = open(path)
    return yaml.load(config_file, Loader=yaml.FullLoader)



