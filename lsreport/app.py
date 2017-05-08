from flask import Flask
from flask_assets import Environment, Bundle

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.cfg', silent=True)

# Exposing constants to use
VERSION = app.config['VERSION'] = '0.0.1'


# JS Assets part
assets = Environment(app)
js = Bundle("js/jquery-3.2.1.min.js", "js/papaya.min.js", "js/script.js",
            filters='jsmin', output='gen/packed.js')
assets.register('js_all', js)

import lsreport.views
