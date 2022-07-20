
import requests

class File_management:
    """
    Download from url
    """ 

    @classmethod
    def download(self, url, path):
        response = requests.get(url)
        file = open(path, "wb")
        file.write(response.content)
        file.close()
