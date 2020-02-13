from tree.Bouton import Bouton
from flask import redirect, url_for



class Bouton_html(Bouton):
    """
    le bouton de l'application web
    """

    def __init__(this, nom, page, app, liste_info):
        Bouton.__init__(this, nom)
        this.page = page
        this.app = app
        # liste_parametre[0] = faux / [1] = vrai
        this.liste_parametre = [[],[]]
        this.liste_info = this.liste_parametre[0]
        liste_info.append(this.liste_info)


        @this.app.site.route('/'+nom)
        @this.exception_handler
        def bouton():
            #on fait les instructions
            this.do()
            this.change()
            #on change la valeur de l'info
            this.liste_info[0] = this.liste_parametre[this.etat][0]
            print(this.liste_info, "etat = ", this.etat)

            return redirect(url_for(this.page))


    def exception_handler(this, func):
      def wrapper():
        try:
            return func()
        except Exception as e:
            error_code = getattr(e, "code", 500)
            logger.exception("Service exception: %s", e)
            r = dict_to_json({"message": e.message, "matches": e.message, "error_code": error_code})
            return Response(r, status=error_code, mimetype='application/json')
      # Renaming the function name:
      wrapper.__name__ = this.nom
      return wrapper

    def add_param(this, param_vrai, param_faux):
        this.liste_parametre[0].append(param_faux)
        this.liste_parametre[1].append(param_vrai)
        print(this.liste_parametre)


