import sys
sys.path.insert(0, '/home/pi/maison')
# on lance l'arbre et les inters
from utils.Data_change.Create_tree import get_tree
get_tree()
from Main import app as application
