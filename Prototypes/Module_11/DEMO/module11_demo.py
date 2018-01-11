import scipy.io as sio
import inc.module11 as module11
import inc.simens_dadm as smns

if __name__ == "__main__":

    #mat_data = sio.loadmat('dane/brain_scan.mat')
    #mat_data = mat_data['t2_volume']
    mat_data = sio.loadmat('dane/segmentationMask.mat')
    mat_data = mat_data['imageMaskFull']
    struct = smns.mri_struct()
    struct.segmentation = mat_data
    result1 = module11.main11(struct)
