import json
import logging
import re
from collections import namedtuple
from pathlib import Path

import nibabel as nib
import numpy as np

Scan = namedtuple('Scan', ['ct_image', 'pet_image', 'label_image', 'vox_size'])
NPZ_PATH = Path.cwd() / 'lsreport/static/image_data/npz'


def read_json():
    """ Reads the json summary file used for the index.html. """
    logging.debug('reading json summary')
    json_files = [j for j in NPZ_PATH.glob('**/*.json')]
    return [_parse_json(i) for i in json_files]


def _parse_json(json_file):
    with open(json_file) as f:
        values = json.load(f)
        values['acc_number'] = _parse_acc_number(json_file.parents[0].name)
        return values


def _parse_acc_number(dir_name):
    matches = re.search('.*ACC(.*)$', dir_name)
    return matches.group(1)


def image_request(acc_number, image_type):
    """ Returns a tuple with the folder and the file name of the requested
    accession number. If nothing can be found Nothing will be returned.
    """
    image_file = _exists_image_file(acc_number, image_type)
    if image_file:
        return image_file.parents[0], image_file.name
    else:
        npz_file = _exists_npz(acc_number)
        if npz_file:
            scan = _extract(npz_file)
            _petct_base64(npz_file.parents[0], scan)
            return npz_file.parents[0], _image_file_name(image_type)
        else:
            return None


def _exists_image_file(acc_number, image_type):
    folder = '*' + acc_number + '/'
    file_name = _image_file_name(image_type)
    result = list(NPZ_PATH.glob(folder + file_name))
    return result[0] if result else []


def _image_file_name(image_type):
    if image_type == 'ct':
        return 'ct.nii.gz'
    elif image_type == 'pet':
        return 'pet.nii.gz'
    elif image_type == 'label':
        return 'label.nii.gz'


def _exists_npz(acc_number):
    folder = '*' + acc_number + '/'
    file_name = 'lsa.npz'
    result = list(NPZ_PATH.glob(folder + file_name))
    return result[0] if result else []


def _petct_base64(dir_name, in_petct):
    # type: Scan -> Dict[str, str]
    out_paths = {}
    for c_img, c_file in zip([in_petct.ct_image, in_petct.pet_image, in_petct.label_image],
                             ['ct', 'pet', 'label']):
        file_name = dir_name / (c_file + '.nii.gz')
        with open(file_name, mode='w+') as tfile:
            nib.save(_wrap_array(c_img, in_petct.vox_size, name=c_file), tfile.name)
            out_paths[c_file] = tfile.name
    return out_paths


def _wrap_array(in_arr, vox_size, xs=1, ys=1, zs=1, name='junk'):
    t_img = nib.Nifti1Image(in_arr, affine=np.eye(4))
    n_vox_size = xs*vox_size[0], ys*vox_size[1], zs*vox_size[2]
    t_img.header.set_zooms(n_vox_size)
    t_img.header.set_xyzt_units('mm')
    t_img.header['db_name'] = name
    t_img.set_filename(name)
    return t_img


def _extract(npz_file):
    # type: str -> Scan
    with np.load(npz_file) as np_file:
        return Scan(ct_image=np_file['CT'],
                    pet_image=np_file['PET'],
                    label_image=np_file['Labels'],
                    vox_size=np.roll(np_file['spacing'], 1))

