import scipy.io as sio


class mri_struct:
	"""A class for storing structural MRI data.
	structural_data is an array where the structural data are held (complex numbers)
	compression_rate is subsampling rate of the data (1 indicates no subsampling)
	coils_n is a number of coils used for data acquisition
	sensitivity_maps are sensitivity profiles of the coils
	noise_map is the estimated noise map
	skull_stripping_mask is a binary mask - the result of skull stripping module
	segmentation is a matrix with segmentation module result
	biomarkers is the result of diffusion tensor imaging module
	"""
	def __init__(self, structural_data = (), compression_rate = 1, coils_n = 0, sensitivity_maps = []):
		self.structural_data = structural_data
		self.compression_rate = compression_rate
		self.coils_n = coils_n
		self.sensitivity_maps = sensitivity_maps

		self.noise_map = []
		self.skull_stripping_mask = []
		self.segmentation = []
		self.biomarkers = []

class mri_diff(mri_struct):
	"""A class for storing diffusion MRI data.
	
	structural_data is an array where the structural data are held (complex numbers)
	compression_rate is subsampling rate of the data (1 indicates no subsampling)
	coils_n is a number of coils used for data acquisition
	sensitivity_maps are sensitivity profiles of the coils
	diffusion_data is the dMRI data
	gradients are directions of Diffusion MRI gradients
	b_value is the intensivity factor
	
	noise_map is the estimated noise map
	skull_stripping_mask is a binary mask - the result of skull stripping module
	segmentation is a matrix with segmentation module result
	biomarkers is the result of diffusion tensor imaging module
	"""
	def __init__(self, raw_data = (), compression_rate = 1, coils_n = 0, sensitivity_maps = [], gradients = [], b_value = 0):
		self.structural_data = raw_data[:,:,0,:]
		self.compression_rate = compression_rate
		self.coils_n = coils_n
		self.sensitivity_maps = sensitivity_maps

		self.diffusion_data = raw_data[:,:,1:,:]
		self.gradients = gradients
		self.b_value = b_value

		self.noise_map = []
		self.skull_stripping_mask = []
		self.segmentation = []
		self.biomarkers = []

def mri_read (filename):
	mfile = sio.loadmat(filename)
	if('raw_data' in mfile and 'r' in mfile and 'L' in mfile and 'sensitivity_maps' in mfile):
		if('gradients' in mfile and 'b_value' in mfile):
			return mri_diff(mfile['raw_data'], mfile['r'], mfile['L'], mfile['sensitivity_maps'], mfile['gradients'], mfile['b_value'])
		else:
			return mri_struct(mfile['raw_data'], mfile['r'], mfile['L'], mfile['sensitivity_maps'])
	else:
		return "Error: could not recognize data in file"
		
	# TODO: ADD FUNCTIONS FOR EASY DATA ACCESS IN CLASSES.