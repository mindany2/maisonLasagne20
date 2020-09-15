from tree.Tree import Tree
from utils.spotify.Spotify import Spotify
from utils.Data_change.Create_tree import get_tree
from utils.Data_change.Create_config import get_config_carte

get_config_carte()
get_tree()
Spotify.init()

from tree.utils.Serveur import Serveur
