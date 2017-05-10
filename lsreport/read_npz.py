import base64
import os
import glob
import logging
import json
import numpy as np
import nibabel as nib

from pathlib import Path



def read_json():
    logging.debug('reading json summary')
    path = Path.cwd() / 'lsreport/static/image_data/npz'
    json_files = [j for j in path.glob('**/*.json')]
    return [parse_json(i) for i in json_files]


def parse_json(json_file):
    print(json_file)
    print(type(json_file))
    print(json_file.parents[0].name)
    with open(json_file) as f:
        values = json.load(f)
        values['dir_name'] = json_file.parents[0].name
        return values


def read_npz(npz_file, image_type):
    path = Path.cwd() / 'lsreport/static/image_data/npz/' / npz_file
    return parse(list(path.glob('**/*.npz'))[0], image_type)


def parse(npz_file, image_type):
    print('parsing', npz_file)
    with np.load(npz_file) as np_file:
        print(np_file.keys())
        label_img = np_file['Labels']
        ct_img = np_file['CT']
        pet_img = np_file['PET']
        label_names = [i.decode('utf-8') for i in np_file['label_names']]
        vox_size = np.roll(np_file['spacing'], 1)
        clinical_staging = 'Missing!'\
            if 'clinical_staging' not in np_file.keys()\
            else np_file['clinical_staging'].tolist()

        if clinical_staging is None:
            clinical_staging = 'Missing!'
        return 'foo'


