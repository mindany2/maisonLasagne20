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
            jsdata = request.form['javascript_data']
            section, button = jsdata.split(".")
            self.manager.press_button(section, button)
            self.manager.pack()
            # TODO send to the js infos to no reload the page
            return {}

    def run(self):
        self.site.run()

    def get_site(self):
        return self.site


