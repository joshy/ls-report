import json
from requests import get
from flask import render_template, request


from lsreport.app import app, VERSION


@app.route('/')
def main():
    """ Renders the initial page. """
    return render_template('index.html',
                           title='LungStage Report',
                           version=VERSION
                          )
