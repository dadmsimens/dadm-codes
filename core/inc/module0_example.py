from . import simens_dadm as smns

def main0(mri_input, other_arguments = None):

    if (isinstance(mri_input, smns.mri_diff)): # instructions for diffusion mri

    # isinstance(mri_input, smns.mri_struct) returns TRUE for diffusion AND structural MRI because of inheritance.
    # It should be used if you have some code to work with BOTH structural and diffusion data (which may be frequent).

        mri_output = mri_input
        print("This file contains diffusion MRI")
        #some_code

    elif (isinstance(mri_input, smns.mri_struct)): # instructions specific for structural mri. The case of diffusion MRI is excluded here by elif.
        mri_output = mri_input
        print("This file contains structural MRI")
        #some_code
    else:
        return "Unexpected data format in module number 0!"

    return mri_output