from cryptography.fernet import Fernet
import os
import yaml

PATH = "data/.secret.yaml"
VARIABLE = "HOME_PASSWORD"

class Secrets:
    """
    Decode a secret file
    with the password in the environnement variable "HOME_PASSWORD"
    """
    def __init__(self):
        with open(PATH, "rb") as file_pass:
            source = file_pass.read()
            key = os.environ.get(VARIABLE)
            if not(key):
                raise(ValueError("The {} is not on environnement variable..".format(VARIABLE)))
            self.secrets = decrypt(key, source).decode("utf-8")
        # cut the secrets
        self.secrets = yaml.safe_load(self.secrets)

    def get_spotify_secret(self):
        return self.secrets.get("SPOTIFY")

def create_key():
    """
    Generates a key to add to the variable environnement
    """
    key = Fernet.generate_key()
    print("Your key is : {}\
        \n you need to add it to your variable environnement {} with :\
        \n \"export {}={}\" in your ~/.bashrc".format(str(key), VARIABLE, VARIABLE, str(key)))

def encrypt(key, source):
    return Fernet(key).encrypt(source)

def decrypt(key, source):
    return Fernet(key).decrypt(source)

if __name__ == "__main__":
    secret = Secrets()

