import io
import os
import logging

from glob import glob


def read_nifti(filename):
    """ Read and return content of file. """
    logging.debug('reading in nifti file with id {}'.format(filename))
    nifti_file = glob('**/' + filename + '*.*', recursive=True)
    if nifti_file:
        with open(nifti_file[0], mode='rb') as image_file:
            #data = image_file.read()

            return io.BytesIO(image_file.read())
    else:
        print('not found')
        return None

