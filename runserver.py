"""
Module to run the application. Defines also logging configuration.
"""
from lsreport.log import configure
from lsreport.app import app

if not app.debug:
    configure(app)

app.run(host='0.0.0.0')
