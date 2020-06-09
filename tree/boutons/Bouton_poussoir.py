from tree.boutons.Bouton import Bouton
from threading import Thread
from tree.utils.Dico import Dico
from tree.scenario.Scenario import MARQUEUR

class Bouton_poussoir(Bouton):
    """
    bouton avec une liste de scénario, il en faut obligatoirement un seul de chaque type
    """
    def __init__(self, nom, env, scenar_on, scenar_off):
        Bouton.__init__(self, nom)
        self.scenars = Dico()
        self.env = env
        # scenar_on peut avoir un marqueur déco ou pas
        self.scenar_on = scenar_on
        self.scenar_off = scenar_off

    def etat_env(self):
        return self.env.etat()

    def press(self):
        # on décide que le premier element de la liste, (celui renseigner en premier)
        # est ce que l'on souhaite faire en priorité :
        # off / déco
        # off / on

        if self.scenar_on.marqueur != self.etat_env():
            if self.scenar_on.marqueur == MARQUEUR.ON:
                return self.lancer_scenar(self.scenar_on)
            elif self.scenar_on.marqueur == MARQUEUR.DECO:
                if self.etat_env() == MARQUEUR.ON:
                    # on ne doit rien faire, On est prioritaire, donc on stocke
                    # juste ce scenar dans le suivant pour retourner à cet état si on éteint
                    if self.env.etat_prec() == MARQUEUR.DECO:
                        # on doit dire que le prochain eteint
                        self.env.change_scenario_prec(self.scenar_off)
                    else: 
                        # on stocke le déco
                        self.env.change_scenario_prec(self.scenar_on)
                    return None
                else:
                    # on était off, on allume donc
                    return self.lancer_scenar(self.scenar_on)
            else: 
                # le scenar on faut off, donc on eteint
                return self.lancer_scenar(self.scenar_on)
        else:
            # on doit eteindre, mais attention aux déco
            if self.etat_env() == MARQUEUR.DECO:
                # on eteint
                return self.lancer_scenar(self.scenar_off)
            else:
                # on est ON
                if self.env.etat_prec() == MARQUEUR.DECO:
                    # on remet cette déco là
                    return self.lancer_scenar(self.env.get_scenario_prec())
                else:
                    # on eteint
                    return self.lancer_scenar(self.scenar_off)


    def lancer_scenar(self, scenar):
        process = Thread(target=scenar.do)
        process.start()
        return scenar

    def show(self):
        print("bouton poussoir")
        super.show()






