from tree.Bouton import Bouton
from flask import redirect, url_for



class Bouton_html(Bouton):
    """
    le bouton de l'application web
    """

    def __init__(self, nom, page, app, liste_info):
        Bouton.__init__(self, nom)
        self.page = page
        self.app = app
        # liste_parametre[0] = faux / [1] = vrai
        self.liste_parametre = [[],[]]
        self.liste_info = self.liste_parametre[0]
        liste_info.append(self.liste_info)


        @self.app.site.route('/'+nom)
        @self.exception_handler
        def bouton():
            #on fait les instructions
            self.do()
            self.change()
            #on change la valeur de l'info
            self.liste_info = self.liste_parametre[self.etat]

            return redirect(url_for(page))


    def exception_handler(self, func):
      def wrapper():
        try:
            return func()
        except Exception as e:
            error_code = getattr(e, "code", 500)
            logger.exception("Service exception: %s", e)
            r = dict_to_json({"message": e.message, "matches": e.message, "error_code": error_code})
            return Response(r, status=error_code, mimetype='application/json')
      # Renaming the function name:
      wrapper.__name__ = self.nom
      return wrapper

    def add_param(self, param_vrai, param_faux):
        self.liste_parametre[0].append(param_faux)
        self.liste_parametre[1].append(param_vrai)


