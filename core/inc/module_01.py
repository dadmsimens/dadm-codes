import simens_dadm as smns
import scipy.io as sio
import numpy as np
from numpy.linalg import inv
from scipy import ndimage

def run_module(mri_input, other_arguments = None):

    if (isinstance(mri_input, smns.mri_diff)): 
        r_factor =  np.squeeze(mri_input.compression_rate)
        L_factor = np.squeeze(mri_input.coils_n)
        mri_diff_data = mri_input.diffusion_data
        mri_struct_data = mri_input.structural_data
        sens_maps = mri_input.sensitivity_maps
        
        dim = np.shape(mri_diff_data)
        if len(np.shape(mri_diff_data)) == 5:
            data = np.zeros((dim[0], dim[1], dim[2]+1, dim[3], dim[4]))
            data = np.concatenate((mri_diff_data, mri_struct_data[:,:,:,None,:]), axis=3)
        elif len(np.shape(mri_diff_data)) == 4:
            data = np.zeros((dim[0], dim[1], dim[2]+1, dim[3]))
            data = np.concatenate((mri_diff_data, mri_struct_data[:,:,None,:]), axis=2)

        dim = np.shape(data)
        
        if len(dim) == 5:
            img_data = np.zeros((dim[0], dim[1], dim[2], dim[3], dim[4]), dtype=np.complex)
        elif len(dim)== 4:
            img_data = np.zeros((dim[0], dim[1], dim[2], dim[3]), dtype=np.complex)

        if len(dim) == 5:
            for ll in range(0,dim[4]):
                for gg in range(0,dim[3]):
                    for ss in range(0,dim[2]):
                        img_data[:,:,ss,gg,ll] = np.fft.ifft2(data[:,:,ss,gg,ll])
        elif len(dim) == 4:
            for ll in range(0,dim[3]):
                for gg in range(0,dim[2]):
                    img_data[:,:,gg,ll] = np.fft.ifft2(data[:,:,gg,ll])
                    
        Ss = np.zeros((L_factor, 1))
        C = np.zeros((L_factor, r_factor))
        Sr = np.zeros((r_factor, 1)) 
        FOVy = dim[0]
        reg_val = 0.005
        I = np.eye(r_factor)        
        
        if len(dim) == 5:
            recon_img_LSE = np.zeros((dim[1], dim[1], dim[2], dim[3]), dtype=np.double)
            med_filt_LSE = np.zeros((dim[1], dim[1], dim[2], dim[3]), dtype=np.double)
            recon_img_Tikhonov = np.zeros((dim[1], dim[1], dim[2], dim[3]), dtype=np.double)
        elif len(dim) == 4:
            recon_img_LSE = np.zeros((dim[1], dim[1], dim[2]), dtype=np.double)
            med_filt_LSE = np.zeros((dim[1], dim[1], dim[2]), dtype=np.double)
            recon_img_Tikhonov = np.zeros((dim[1], dim[1], dim[2]), dtype=np.double)
            
        if len(dim) == 5:
            for n in range(0,dim[0]):
                for m in range(0,dim[1]):
                    for ss in range(0,dim[2]):
                        for gg in range(0,dim[3]):
                            ind = np.arange(n, dim[1],FOVy)
                            Cc=np.absolute(sens_maps[ind,m,:])
                            C=np.absolute(np.transpose(Cc))
                            Ss=np.absolute(img_data[n,m,ss,gg,:])
                            Sr = np.transpose(inv(Cc@C)@(Cc@Ss))
                            recon_img_LSE[ind,m,ss,gg] = Sr
            
            for ss in range(0,dim[2]):
                for gg in range(0,dim[3]):
                    med_filt_LSE[:,:,ss,gg] =  ndimage.median_filter(recon_img_LSE[:,:,ss,gg], 3)
                
            for n in range(0,dim[0]):
                for m in range(0,dim[1]):
                    for ss in range(0,dim[2]):
                        for gg in range(0,dim[3]):
                            ind = np.arange(n, dim[1],FOVy)
                            Cc=np.absolute(sens_maps[ind,m,:])
                            C=np.absolute(np.transpose(Cc))
                            Ss=np.absolute(img_data[n,m,ss,gg,:])
                            ref_img = med_filt_LSE[ind,m,ss,gg]
                            Sr = np.transpose(ref_img + inv(Cc@C+reg_val*I)@(Cc@(Ss-C@ref_img)))
                            recon_img_Tikhonov[ind,m,ss,gg] = Sr

        elif len(dim) == 4:
            for n in range(0,dim[0]):
                for m in range(0,dim[1]):
                    for gg in range(0,dim[2]):
                        ind = np.arange(n, dim[1],FOVy)
                        Cc=np.absolute(sens_maps[ind,m,:])
                        C=np.absolute(np.transpose(Cc))
                        Ss=np.absolute(img_data[n,m,gg,:])
                        Sr = np.transpose(inv(Cc@C)@(Cc@Ss))
                        recon_img_LSE[ind,m,gg] = Sr
            
            for gg in range(0,dim[2]):
                med_filt_LSE[:,:,gg] =  ndimage.median_filter(recon_img_LSE[:,:,gg], 3)

            for n in range(0,dim[0]):
                for m in range(0,dim[1]):
                    for gg in range(0,dim[2]):
                        ind = np.arange(n, dim[1],FOVy)
                        Cc=np.absolute(sens_maps[ind,m,:])
                        C=np.absolute(np.transpose(Cc))
                        Ss=np.absolute(img_data[n,m,gg,:])
                        ref_img = med_filt_LSE[ind,m,gg]
                        Sr = np.transpose(ref_img + inv(Cc@C+reg_val*I)@(Cc@(Ss-C@ref_img)))
                        recon_img_Tikhonov[ind,m,gg] = Sr
        
        if len(np.shape(recon_img_Tikhonov)) == 4:
            mri_input.mri_diffusion_data = np.absolute(recon_img_Tikhonov[:,:,:,1:]) 
            mri_input.mri_structural_data = np.absolute(recon_img_Tikhonov[:,:,:,0])
        elif len(np.shape(recon_img_Tikhonov)) == 3:
            mri_input.mri_diffusion_data = np.absolute(recon_img_Tikhonov[:,:,1:]) 
            mri_input.mri_structural_data = np.absolute(recon_img_Tikhonov[:,:,0])

        return mri_input

    elif (isinstance(mri_input, smns.mri_struct)): 
        # mri_structural.raw_data = run_reconstruction_struct(mri_struct)
        r_factor =  np.squeeze(mri_input.compression_rate)
        L_factor = np.squeeze(mri_input.coils_n)
        mri_struct_data = mri_input.structural_data
        sens_maps = mri_input.sensitivity_maps
        
        dim = np.shape(mri_struct_data)
        if len(dim) == 4:
            img_data = np.zeros((dim[0], dim[1], dim[2], dim[3]), dtype=np.complex)                        
        elif len(dim) == 3:
            img_data = np.zeros((dim[0], dim[1], dim[2]), dtype=np.complex)

        if len(dim) == 4:
            for ll in range(0,dim[3]):
                for ss in range(0,dim[2]):
                    img_data[:,:,ss,ll] = np.fft.ifft2(mri_struct_data[:,:,ss,ll])
        elif len(dim) == 3:
            for ll in range(0,dim[2]):
                img_data[:,:,ll] = np.fft.ifft2(mri_struct_data[:,:,ll])
        
        Ss = np.zeros((L_factor, 1))
        C = np.zeros((L_factor, r_factor))
        Sr = np.zeros((r_factor, 1)) 
        FOVy = dim[0]
        reg_val = 0.005
        I = np.eye(r_factor)
        
        if len(dim) == 4:
            recon_img_LSE = np.zeros((dim[1], dim[1], dim[2]), dtype=np.double)
            med_filt_LSE = np.zeros((dim[1], dim[1], dim[2]), dtype=np.double)
            recon_img_Tikhonov = np.zeros((dim[1], dim[1], dim[2]), dtype=np.double)
        elif len(dim) == 3:
            recon_img_LSE = np.zeros((dim[1], dim[1]), dtype=np.double)
            med_filt_LSE = np.zeros((dim[1], dim[1]), dtype=np.double)
            recon_img_Tikhonov = np.zeros((dim[1], dim[1]), dtype=np.double)

        if len(dim) == 4:
            for n in range(0,dim[0]):
                for m in range(0,dim[1]):
                    for ss in range(0,dim[2]):
                        ind = np.arange(n, dim[1],FOVy)
                        Cc=np.absolute(sens_maps[ind,m,:])
                        C=np.absolute(np.transpose(Cc))
                        Ss=np.absolute(img_data[n,m,ss,:])
                        Sr = np.transpose(inv(Cc@C)@(Cc@Ss))
                        recon_img_LSE[ind,m,ss] = Sr
            
            for ss in range(0,dim[2]):
                med_filt_LSE[:,:,ss] =  ndimage.median_filter(recon_img_LSE[:,:,ss], 3)
                
            for n in range(0,dim[0]):
                for m in range(0,dim[1]):
                    for ss in range(0,dim[2]):
                        ind = np.arange(n, dim[1],FOVy)
                        Cc=np.absolute(sens_maps[ind,m,:])
                        C=np.absolute(np.transpose(Cc))
                        Ss=np.absolute(img_data[n,m,ss,:])
                        ref_img = med_filt_LSE[ind,m,ss]
                        Sr = np.transpose(ref_img + inv(Cc@C+reg_val*I)@(Cc@(Ss-C@ref_img)))
                        recon_img_Tikhonov[ind,m,ss] = Sr

        elif len(dim) == 3:
            for n in range(0,dim[0]):
                for m in range(0,dim[1]):
                    ind = np.arange(n, dim[1],FOVy)
                    Cc=np.absolute(sens_maps[ind,m,:])
                    C=np.absolute(np.transpose(Cc))
                    Ss=np.absolute(img_data[n,m,:])
                    Sr = np.transpose(inv(Cc@C)@(Cc@Ss))
                    recon_img_LSE[ind,m] = Sr
                    
            med_filt_LSE =  ndimage.median_filter(recon_img_LSE, 3)

            for n in range(0,dim[0]):
                for m in range(0,dim[1]):
                    ind = np.arange(n, dim[1],FOVy)
                    Cc=np.absolute(sens_maps[ind,m,:])
                    C=np.absolute(np.transpose(Cc))
                    Ss=np.absolute(img_data[n,m,:])
                    ref_img = med_filt_LSE[ind,m]
                    Sr = np.transpose(ref_img + inv(Cc@C+reg_val*I)@(Cc@(Ss-C@ref_img)))
                    recon_img_Tikhonov[ind,m] = Sr

        mri_input.structural_data = np.absolute(recon_img_Tikhonov) 
        
        return mri_input
    
    else:
        return "Unexpected data format in module number 0!"
