import logging

from flask import render_template, jsonify, request

from lsreport.app import app, VERSION
from lsreport.read_npz import read_json, read_npz
from lsreport.read_nifti import read_nifti


@app.route('/')
def main():
    """ Renders the initial page. """
    niftis = read_nifti()
    npz_jsons = read_json()

    return render_template('index.html',
                           title='LungStage Report',
                           niftis=niftis,
                           npz_jsons=npz_jsons,
                           version=VERSION
                          )


@app.route('/nifti_viewer')
def nifti_viewer():
    """ Renders medical image view for nifti. """
    return render_template('nifti_viewer.html')


@app.route('/npz_viewer')
def npz_viewer():
    """ Renders medical image view for npz. """
    return render_template('npz_viewer.html')


@app.route('/image_data/<dir>')
def npz(dir):
    logging.debug('go dir %d', dir)
    image_type = request.args.get('image_type', 'ct')
    apect = read_npz(dir, image_type)
    return jsonify(apect)
