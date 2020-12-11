from flask import Flask, redirect, url_for, request, render_template

class App:

    def  __init__(self, manager):
        self.manager = manager
        self.site = Flask(__name__)

        @self.site.route('/')
        def index():
            self.manager.reload()
            return render_template('index.html', manager = self.manager)

        @self.site.route('/press_button', methods = ['POST'])
        def press_button():
            jsdata = request.form['javascript_data']
            print(jsdata)
            line, button = jsdata.split(".")
            self.manager.press_button(line, button)
            return {"change":[{"id": "myButton2", "name" : "lol"},{"id": jsdata, "name" : "coucou"}]}


    def run(self):
        self.site.run()

    def get_site(self):
        return self.site

