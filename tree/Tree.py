from tree.utils.Liste_radios import Liste_radios
from tree.utils.Liste import Liste
from threading import Thread
from utils.Logger import Logger

class Tree:
    liste_envi = Liste()
    liste_modes = Liste_radios()

    @classmethod
    def show(self):
        print("modes : ")
        self.liste_modes.show()
        print("Environnements : ")
        self.liste_envi.show()

    @classmethod
    def get_mode(self, nom_mode):
        return self.liste_modes.get(nom_mode)

    @classmethod
    def change_mode_select(self, mode):
        self.liste_modes.change_select(mode)
        Logger.info("Changement de mode : " + self.get_current_mode().nom)

    @classmethod
    def press_inter(self, nom_inter, etat):
        Logger.debug("on press l'inter "+nom_inter)
        # on recupère tous les boutons
        for env in self.liste_envi:
            if env.get_preset_select().principal(nom_inter):
                break
        etat_env = env.etat()
        for env in self.liste_envi:
            env.get_preset_select().press_inter(nom_inter,etat_env, etat)

    @classmethod
    def add_mode(self, mode):
        self.liste_modes.add(mode)

    @classmethod
    def get_current_mode(self):
        return self.liste_modes.selected()

    @classmethod
    def reload_modes(self):
        self.change_mode_select(self.get_current_mode())
        # on met les environnements dans le même mode
        for env in self.liste_envi:
            env.change_mode()

    @classmethod
    def get_env(self, env):
        return self.liste_envi.get(env)

    @classmethod
    def get_noms_envi(self):
        return [env.nom for env in self.liste_envi]

    @classmethod
    def get_infos_envi(self):
        return [[env.nom,env.style, env.nb_boutons_html()] for env in self.liste_envi]

    @classmethod
    def press_bouton_html(self, nom_env, index):
        if nom_env != "mode":
            self.get_env(nom_env).get_preset_select().press_bouton_html(index)
        else:
            self.liste_modes.selected().press_bouton_mode()

    @classmethod
    def reload_html(self):
        for env in self.liste_envi:
            env.get_preset_select().reload_html()

    @classmethod
    def get_bouton_html(self, nom_env, index):
        if nom_env != "mode":
            return self.get_env(nom_env).get_preset_select().get_bouton_html(index)
        else:
            return self.liste_modes.selected().bouton_change_html

    @classmethod
    def get_scenar(self, nom_env, nom_scenar):
        return self.get_env(nom_env).get_scenar(nom_scenar)
