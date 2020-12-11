import os

def list_files(path):
    return [name for name in os.listdir(path) if (os.path.isfile("{}/{}".format(path,name)))]

def list_folders(path):
    return [name for name in os.listdir(path) if (os.path.isdir("{}/{}".format(path,name)))]

