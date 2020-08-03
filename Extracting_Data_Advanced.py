#!/usr/bin/env python
# coding: utf-8

# In[1]:


from utils.Variable_setup import *
from utils.Extraction_functions import *
import pickle
import os


# In[2]:


metrics = ['DKI_Thresholded',  'MAPMRI',  'NODDI']
submetrics = DKI_Metrics + MAPMRI_Metrics + NODDI_Metrics


# ## Initialize nan filled arrays

# In[3]:


import numpy as np
Extracted_Data = {}
Extracted_Data['Description'] = ' ##SAGAB## Dict containing ROI-Wise extracted values for Advanced Metrics'

for proc in preprocs:
    Extracted_Data[proc] = {}
    for met in metrics:
        Extracted_Data[proc][met] = {}
        for submet in submetrics:
            if not os.path.isdir(os.path.join(Advanced_maps_path,proc,met,submet)):
                continue
            else:
                Extracted_Data[proc][met][submet] = {}
                for ROI in ROIS:
                    Extracted_Data[proc][met][submet][ROI] = np.full([num_subjects, num_sessions], np.nan)


# In[5]:


failed_files = []
for ROI in ROIS:
    fROI = os.path.join(ROIs_path,ROI)
    for proc in preprocs:
        for met in metrics:
            for submet in submetrics:
                
                #Save every submetric
                with open(os.path.join(data_path,'SAGAB_Advanced_Metric_ROIWISE_Extracted_Data.pckl'), 'wb') as handle:
                    pickle.dump(Extracted_Data, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    
                if not os.path.isdir(os.path.join(Advanced_maps_path,proc,met,submet)):
                    continue
                else:
                    for s, ses in enumerate(sess):
                        fpath = os.path.join(Advanced_maps_path,proc,met,submet)                
                        for i in range(1,num_subjects+1):
                            substring = 'sub-'+str(i).zfill(2)+'_'+ses+'*'
                            file = find(substring, fpath)
                            if not file:
                                continue
                            else:
                                file = ''.join(file)
                                if os.path.isfile(os.path.join(os.getcwd(),'stat_result.json')):
                                    try:
                                        os.remove(os.path.join(os.getcwd(),'stat_result.json'))
                                    except:
                                        pass
                                try:
                                    Extracted_Data[proc][met][submet][ROI][i-1,s] = FSLROI_Image(file, fROI)
                                except:
                                    print('failed file: ', file)
                                    failed_files.append(file)
print('finished')
print('#############')
print(failed_files)
print('#############')


# ## This will save a pickle

# In[6]:


import pickle


with open(os.path.join(data_path,'SAGAB_Advanced_Metric_ROIWISE_Extracted_Data.pckl'), 'wb') as handle:
    pickle.dump(Extracted_Data, handle, protocol=pickle.HIGHEST_PROTOCOL)

