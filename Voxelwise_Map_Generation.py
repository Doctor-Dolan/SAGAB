#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from utils.Variable_setup import *
from utils.Extraction_functions import *
from utils.ICC_functions import *
import numpy as np
import os
import nibabel as nib


# In[ ]:


mask = nib.load(Template_Mask)
aff = mask.affine
mask = mask.get_fdata()
mask = mask[:].astype(bool)


# In[ ]:


metrics = Metrics
paradigms = Metrics_paradigms + Extracted_Metrics_paradigms


# ## Makes the file locations array for a given image type

# In[ ]:


proc='GDT'
digm='Single_Band'
met='Fractional_Anisotropy'
sessions=['ses-1', 'ses-2', 'ses-3']

file_locations = np.full([30,3], np.nan, dtype=object)
for sid, ses in enumerate(sessions):
    fpath = os.path.join(Basic_maps_path,proc,digm,met,ses)
    for sub in range(1,num_subjects+1):
        substring = 'sub-'+str(sub).zfill(2)+'_'+ses+'*'
        file = find(substring, fpath)
        if not file:
            continue
        else:
            file_locations[sub-1,sid] = file[0]


# In[ ]:


#Loads all niftii images into a 5D numpy
whole_cohort = load_whole_cohort(file_locations)


# In[ ]:


#Calculates ICC, CVws, CVbs on 5D numpy
Curr_ICC, Curr_CVws, Curr_CVbs = ICC_Voxelwise_Vector(whole_cohort,mask)


# In[ ]:


sessions=['ses-1', 'ses-2', 'ses-3']
Voxelwise_ICC = {}
Voxelwise_CVws = {}
Voxelwise_CVbs = {}

for proc in preprocs:
    print(proc)
    Voxelwise_ICC[proc] = {}
    Voxelwise_CVws[proc] = {}
    Voxelwise_CVbs[proc] = {}

    for digm in paradigms:
        print(digm)
        Voxelwise_ICC[proc][digm] = {}
        Voxelwise_CVws[proc][digm] = {}
        Voxelwise_CVbs[proc][digm] = {}
        
        for met in metrics:
            print(met)

            #Load file locations into array
            file_locations = np.full([30,3], np.nan, dtype=object)
            for sid, ses in enumerate(sessions):
                fpath = os.path.join(Basic_maps_path,proc,digm,met,ses)
                for sub in range(1,num_subjects+1):
                    substring = 'sub-'+str(sub).zfill(2)+'_'+ses+'*'
                    file = find(substring, fpath)
                    if not file:
                        continue
                    else:
                        file_locations[sub-1,sid] = file[0]
                        
            #Loads all niftii images into a 5D numpy
            whole_cohort = load_whole_cohort(file_locations)
            
            #Calculates ICC, CVws, CVbs on 5D numpy
            Curr_ICC, Curr_CVws, Curr_CVbs = ICC_Voxelwise_Vector(whole_cohort,mask)
            
            #Store results
            floc = os.path.join(Voxelwise_maps_path,proc,digm)
            fstring = met
            
            header = nib.Nifti1Header()
            
            Curr_ICC_nii = nib.Nifti1Image(Curr_ICC, aff, header)
            Curr_CVws_nii = nib.Nifti1Image(Curr_CVws, aff, header)
            Curr_CVbs_nii = nib.Nifti1Image(Curr_CVbs, aff, header)
            
            nib.save(Curr_ICC_nii, os.path.join(floc,met+'_ICC.nii'))
            nib.save(Curr_CVws_nii, os.path.join(floc,met+'_CVws.nii'))
            nib.save(Curr_CVbs_nii, os.path.join(floc,met+'_CVbs.nii'))
            
            np.save(os.path.join(floc,met+'_ICC.npy'), Curr_ICC)
            np.save(os.path.join(floc,met+'_CVws.npy'), Curr_CVws)
            np.save(os.path.join(floc,met+'_CVbs.npy'), Curr_CVbs)
            
            Voxelwise_ICC[proc][digm][met] = Curr_ICC
            Voxelwise_CVws[proc][digm][met] = Curr_CVws
            Voxelwise_CVbs[proc][digm][met] = Curr_CVbs
print('finished')


# In[ ]:


import pickle

with open(os.path.join(data_path,'Voxelwise_ICC.pckl'), 'wb') as handle:
    pickle.dump(Voxelwise_ICC, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(os.path.join(data_path,'Voxelwise_CVws.pckl'), 'wb') as handle:
    pickle.dump(Voxelwise_CVws, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(os.path.join(data_path,'Voxelwise_CVbs.pckl'), 'wb') as handle:
    pickle.dump(Voxelwise_CVbs, handle, protocol=pickle.HIGHEST_PROTOCOL)

