import json
from requests import get
from flask import render_template, request, jsonify, send_file


from lsreport.app import app, VERSION
from lsreport.read_npz import read
from lsreport.read_nifti import read_nifti

@app.route('/')
def main():
    """ Renders the initial page. """
    patients = read()
    return render_template('index.html',
                           title='LungStage Report',
                           patients=patients,
                           version=VERSION
                          )


@app.route('/viewer')
def viewer():
    """ Renders medical image view. """
    return render_template('viewer.html')


@app.route('/load/<id>')
def load(id):
    """ Loads the image data and returns a json. """
    data = read_nifti(id)
    if data is not None:

        return send_file(data,
                         attachment_filename='logo.png',
                         mimetype='application/x-nifti')
    else:
        return 'file not found'