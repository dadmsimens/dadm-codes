from .. import simens_dadm as smns

def mymodulefunction(mri_class, other_arguments = None):

	if (isinstance(mri_class, smns.mri_struct)):
		mri_class_modified = mri_class
		print("This file contains structural MRI")
		#some_code
		my_returns = 0
	else:
		print("This file contains diffusion MRI")
		mri_class_modified = mri_class
		#some_code
		my_returns = 0
		#some code

	# https://www.safaribooksonline.com/library/view/python-cookbook-3rd/9781449357337/ch07s04.html
	return mri_class_modified, my_returns