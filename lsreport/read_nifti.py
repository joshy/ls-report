import os
import logging
import glob


def read_nifti():
    logging.debug('reading in reports')
    image_files = os.path.join(os.getcwd(), 'lsreport', 'static', 'image_data', 'nifti', '**', 'IMG*.nii.gz')
    mask_files = os.path.join(os.getcwd(), 'lsreport', 'static', 'image_data', 'nifti', '**', 'MASK*.nii.gz')
    return [(os.path.basename(i), os.path.basename(m))
            for i, m in zip(glob.glob(image_files, recursive=True),
                            glob.glob(mask_files, recursive=True))]



