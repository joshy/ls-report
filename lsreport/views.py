import json
import logging

from requests import get
from flask import render_template, request, jsonify, send_file

from lsreport.app import app, VERSION
from lsreport.read_npz import read
from lsreport.read_nifti import read_nifti


@app.route('/')
def main():
    """ Renders the initial page. """
    niftis = read_nifti()
    print(niftis)
    return render_template('index.html',
                           title='LungStage Report',
                           niftis=niftis,
                           version=VERSION
                          )


@app.route('/viewer')
def viewer():
    """ Renders medical image view. """
    return render_template('viewer.html')

