from flask import Flask, redirect, url_for, request, render_template
from web_app.manager.icons.Icon import TYPE_ICON

class App:

    def  __init__(self, manager, root_path):
        self.manager = manager
        print(root_path)
        self.site = Flask(__name__, root_path=root_path,
                                    template_folder=root_path+"/web_app/templates",
                                    static_folder=root_path+"/data/pages/images")

        @self.site.route('/')
        def index():
            self.manager.pack()
            return render_template('index.html', manager = self.manager, TYPE_ICON = TYPE_ICON)

        @self.site.route('/press_button', methods = ['POST'])
        def press_button():
            id = request.form['id']
            section, button = id.split(",")
            self.manager.press_button(section, button)
            # TODO send to the js infos to no reload the page
            return {}

        @self.site.route('/move_slider', methods = ['POST'])
        def move_slider():
            id = request.form['id']
            value = request.form['value']
            section, button = id.split(",")
            self.manager.move_slider(section, button, int(value))
            # TODO send to the js infos to no reload the page
            return {}

        @self.site.route('/tree_interrupt', methods = ['POST'])
        def interrupt():
            print(request)
            return {"lol":42}


    def run(self):
        self.site.run()

    def get_site(self):
        return self.site


