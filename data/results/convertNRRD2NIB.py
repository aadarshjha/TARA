import nrrd
import nibabel as nib
import os
import sys

for filename in os.listdir(os.getcwd()):
    if filename.endswith(".nrrd"):
        data, header = nrrd.read(filename)
        save_image = nib.Nifti1Image(dataobj = data, affine=None)
        nib.save(save_image, filename.split('.')[0] + '.nii.gz')