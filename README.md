# Image service / Web Viewer

# Setup

## Nifti
Put nifti files under 'static/image_data/nifti'. Sample data can be found
here: https://www.kaggle.com/irrwitz/cnn-with-keras/input

## NPZ
Put npz files under 'static/image_data/npz'. Sample data can only be get
internally. It assumes the following
 * Under the `npz` folder there is a folder with the accession number encoded
   in it, e.g. like `aas_d12_ACC123456789` where `123456789` is the accession
   number. Important is ending with ACC{Number}
 * npz files are called `lsa.npz``
