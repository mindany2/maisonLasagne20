from data_manager.utils.File_yaml import File_yaml

PATH = ".secrets.yaml"

class Secrets:
    """
    Decode a secret file
    with the password in the environnement variable "HOME_PASSWORD"
    """
    def __init__(self, getter):
        self.secrets = File_yaml(getter, PATH)

    def get_spotify_secret(self):
        return self.secrets.get("Spotify", mandatory=True)

