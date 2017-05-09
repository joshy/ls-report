import os
import glob
import logging
import json
import numpy as np
import nibabel as nib

from pathlib import Path
from collections import namedtuple
from scipy.ndimage import zoom, maximum_filter


import matplotlib.pyplot as plt

apetct = namedtuple('AnnotatedPETCT', ['ct_img', 'pet_img', 'lab_img',
                                       'label_names', 'vox_size',
                                       'clinical_staging'])


def read_json():
    logging.debug('reading json summary')
    path = Path.cwd() / 'lsreport/static/image_data/npz'
    json_files = [j for j in path.glob('**/*.json')]
    return [parse_json(i) for i in json_files]


def parse_json(json_file):
    with open(json_file) as f:
        return json.load(f)


def read_npz():
    logging.debug('reading in reports')
    npz_files = os.path.join(os.getcwd(), 'image_data', 'npz', '**', '*.npz')
    return [parse(npz) for npz in glob.glob(npz_files, recursive=True)]


def parse(npz_file):
    print('parsing', npz_file)
    with np.load(npz_file) as np_file:
        print(np_file.keys())
        label_img = np_file['Labels']
        ct_img = np_file['CT']
        pet_img = np_file['PET']
        label_names = [i.decode for i in np_file['label_names']]
        vox_size = np.roll(np_file['spacing'], 1)
        clinical_staging = 'Missing!'\
            if 'clinical_staging' not in np_file.keys()\
            else np_file['clinical_staging'].tolist()

        if clinical_staging is None:
            clinical_staging = 'Missing!'
        return apetct(lab_img=label_img, ct_img=ct_img, pet_img=pet_img,
                      label_names=label_names, vox_size=vox_size,
                      clinical_staging=clinical_staging)


def prepare_petct(in_petct, scale=0.25, make_big=False):
    if not isinstance(scale, list):
        scale = [scale] * 3
    flip_axes = lambda x: x.swapaxes(0, 1).swapaxes(0, 2)[:, :, ::-1]
    n_vox_size = [a/b for a, b in zip(in_petct.vox_size, scale)]
    n_vox_size = n_vox_size[2], n_vox_size[0], n_vox_size[1]
    new_ct = flip_axes(zoom(in_petct.ct_img, scale, order=3)).astype(np.int32)
    new_pet = flip_axes(zoom(in_petct.pet_img, scale, order=3)).astype(np.int32)
    big_labels = maximum_filter(in_petct.label_img, np.ceil(1/np.array(scale))
                                .astype(np.int32))
    new_labels = flip_axes(zoom(big_labels, scale, order=0))
    return apetct(ct_img=new_ct, pet_img=new_pet, label_img=new_labels,
                  vox_size=n_vox_size)


def wrap_array(in_arr, vox_size, xs=1, ys=1, zs=1, name='junk'):
    t_img = nib.Nifti1Image(in_arr, affine=np.eye(4))
    n_vox_size = xs*vox_size[0], ys*vox_size[1], zs*vox_size[2]
    t_img.header.set_zooms(n_vox_size)
    t_img.header.set_xyzt_units('mm')
    t_img.header['db_name'] = name
    t_img.set_filename(name)
    return t_img



def fancy_format(in_str, **kwargs):
    new_str = in_str.replace('{', '{{').replace('}', '}}')
    for key in kwargs.keys():
        new_str = new_str.replace('{{%s}}' % key, '{%s}' % key)
    return new_str.format(**kwargs)


def write_papaya_html(out_file_path, out_blobs, title, clinical_staging_text):
    with open('papaya_base.template', 'r') as pbase:
        all_text = pbase.read()

    with open(out_file_path, 'w') as out_file:
        data_vars = ""
        params = {'encodedImages': []}
        for im_type in ['ct', 'pet', 'lab']:
            im_data = out_blobs[im_type]
            data_vars += 'var {im_type}DataRef = "{im_data}";\n'.format(im_type = im_type, im_data = im_data)
            params["encodedImages"] += ['{im_type}DataRef'.format(im_type = im_type)]
        params["worldSpace"] = False
        #params["ctDataRef"] = {"min": -1024, "max": 1024, "lut": "Grayscale"}
        params["ctDataRef"] = {"min": 40-200, "max": 40+200, "lut": "Grayscale"} # soft tissue window
        params["ctDataRef"] = {"min": -1200, "max": 0, "lut": "Grayscale"} # lung window
        params["petDataRef"] = {"min": 0.3, "max": 5, "lut": "Gold", "alpha": 0.4}
        params["labDataRef"] = {"min": 0.1, "max": 200, "lut": "Blue Overlay", "alpha": 0.8}
        #params["coordinate"] = [42, -52, 29];
        params["kioskMode"] = False
        params["orthogonalTall"] = False
        params["canOpenInMango"] = True
        params["expandable"] = True
        params["showRuler"] = False
        params["showOrientation"] = True
        params["showEULA"] = False
        params["radiological"] = False
        params["mainView"] = "coronal"


        clin_staging_list = ['<li class="list-group-item">{}</li>'.format(cs) for cs in clinical_staging_text.split(',')]
        clin_staging_html = '\n'.join(['<ul class="list-group">']+clin_staging_list+['</ul>'])
        out_file.write(fancy_format(all_text,
                                    data_vars=data_vars,
                                    param_vars=json.dumps(params),
                                    clinical_staging=clin_staging_html,
                                    title=title))



