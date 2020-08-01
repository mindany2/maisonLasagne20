class Trappe:
    """
    modélise la trappe
    """
    def __init__(self):
        # etat = 0 : ferme / etat = 1 : ouvert
        etat = Arduino().send_for_request(MESSAGE_MASTER.demande_etat_trappe)
        Arduino().send(MESSAGE_MASTER.sécurité_trappe_on)   # on met la sécu
        print("etat trappe = "+str(etat))

    def set_secu(self, etat):
        self.sécu = etat
        if self.sécu:
            print("on sécurise")
            Arduino().send(MESSAGE_MASTER.sécurité_trappe_on)
        else:
            print("on désécurise")
            Arduino().send(MESSAGE_MASTER.sécurité_trappe_off)
