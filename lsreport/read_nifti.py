import logging

from pathlib import Path


def read_nifti():
    # type:() -> [(str, str)]
    """ Returns list of tuples, first is image file name, second is mask
    file name.
    """
    logging.debug('reading in niftis')
    path = Path.cwd() / 'lsreport/static/image_data/nifti'
    image_files = path.glob('**/IMG*.nii.gz')
    mask_files = path.glob('**/MASK*.nii.gz')

    return [(i.name, m.name) for i, m in zip(image_files, mask_files)]
