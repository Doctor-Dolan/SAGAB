#!/usr/bin/env python
# coding: utf-8

# In[8]:


import os
from configparser import ConfigParser
parser = ConfigParser()

parser.read('config.ini')
parser.read('./../config.ini')

Basic_maps_path = parser.get('base_vars','Basic_maps_path')
Advanced_maps_path = parser.get('base_vars','Advanced_maps_path')
ROIs_path = parser.get('base_vars','ROIs_path')
Caudate_ROIs_path = parser.get('base_vars','Caudate_ROIs_path')
data_path = parser.get('base_vars','data_path')
num_subjects = int(parser.get('base_vars','num_subjects'))
num_sessions = int(parser.get('base_vars','num_sessions'))


#Generate list of all the ROIs
ROIS = [f for f in os.listdir(path=ROIs_path) if os.path.isfile(os.path.join(ROIs_path,f))]

ROIS = list(filter(lambda k: 'DS' not in k, ROIS))
ROIS = list(filter(lambda k: '.afp' not in k, ROIS))
ROIS = list(filter(lambda k: '.csv' not in k, ROIS))

#Generate list of all the ROIs
Caudate_ROIS = [f for f in os.listdir(path=Caudate_ROIs_path) if os.path.isfile(os.path.join(Caudate_ROIs_path,f))]

Caudate_ROIS = list(filter(lambda k: 'DS' not in k, ROIS))
Caudate_ROIS = list(filter(lambda k: '.afp' not in k, ROIS))
Caudate_ROIS = list(filter(lambda k: '.csv' not in k, ROIS))


# In[ ]:

sess = ['ses-1', 'ses-2', 'ses-3']
preprocs = ['Regular', 'GDT']


Metrics = [ "Axial" , "Fractional_Anisotropy" , "Radial" , "Trace" ]
Extracted_Metrics = [ "Axial" , "Fractional_Anisotropy" , "Radial" , "Trace" ]
Native_Metrics = [ "Axial" , "Fractional_Anisotropy" , "Radial" , "Trace" ]
B0_Removed_Metrics = [ "Axial" , "Fractional_Anisotropy" , "Radial" , "Trace" ]
Jacobians = [ "Jacobians" ]
Extracted_Jacobians = [ "Ext_Jacobians" ]
Advanced_Metrics = [ "DKI" , "DKI_Thresholded" , "NODDI" , "MAPMRI" ]
DKI_Metrics = [ "Radial_Kurtosis" , "Axial_Kurtosis" , "Mean_Kurtosis" , "Kurtosis_Anisotropy" ]
DKI_Thresh_Metrics = [ "Radial_Kurtosis_Thresh" , "Axial_Kurtosis_Thresh" , "Mean_Kurtosis_Thresh", "Kurtosis_Anisotropy_Thresh" ]
MAPMRI_Metrics = [ "Return_To_Plane_Probability" , "Return_To_Origin_Probability" , "Return_To_Axis_Probability" 
                  , "Non_Gaussianity" , "PAth", "Propagator_Anisotropy" , "NGpar" , "NGperp" ]
NODDI_Metrics = [ "Orientation_Dispersion" , "Isotropic_Volume_Fraction" , "IntraCellular_Volume_Fraction" ]


Basic_Metrics_dict = { 'Axial' : 'AD' , "Fractional_Anisotropy" : 'FA' , "Jacobians" : 'JAC' , "Radial" : 'RD' , "Trace" : 'TR' }
Extracted_Metrics_dict = { 'Ext_Axial' : 'AD_ext' , "Ext_Fractional_Anisotropy" : 'FA_ext' , "Ext_Radial" : 'RD_ext' , "Ext_Trace" : 'TR_ext' }
Native_Metrics_dict = { 'Native_Axial' : 'AD_N' , "Native_Fractional_Anisotropy" : 'FA_N' , "Native_Radial" : 'RD_N' , "Native_Trace" : 'TR_N' }
B0_Removed_Metrics_dict = { "B0_Axial" : "AD_B" , "B0_Fractional_Anisotropy" : "FA_B" , "B0_Radial" : "RD_B" , "B0_Trace" : "TR_B" }
Jacobians_Metrics_dict = { "Jacobians" : "JAC" }
Extracted_Jacobians_Metrics_dict = { "Ext_Jacobians" : "JAC_ext" }
DKI_dict = { 'Radial_Kurtosis' : 'RK' , "Axial_Kurtosis" : 'AK' , "Mean_Kurtosis" : 'MK' , "Kurtosis_Anisotropy" : 'KA' }
DKI_Thresh_dict = { 'Radial_Kurtosis_Thresh' : 'RK_T' , "Axial_Kurtosis_Thresh" : 'AK_T' , "Mean_Kurtosis_Thresh" : 'MK_T' , "Kurtosis_Anisotropy_Thresh" : "KA_T" }
MAPMRI_dict = { "Return_To_Plane_Probability" : 'RTPP' , "Return_To_Origin_Probability" : 'RTOP', "Return_To_Axis_Probability" : 'RTAP' ,
                  "Non_Gaussianity" : 'NG' , "PAth" : 'PAth' , "Propagator_Anisotropy" : 'PA' , "NGpar" : 'NGpar' , "NGperp" : 'NGperp' }
NODDI_dict = { "Orientation_Dispersion" : 'OD' , "Isotropic_Volume_Fraction" : 'ISOVF' , "IntraCellular_Volume_Fraction" : 'ICVF' }
Metrics_dict = {'Metrics' : Metrics, 'Ext_Metrics' : Extracted_Metrics, 'Native' : Native_Metrics, 'B0_Removed' : B0_Removed_Metrics,
             'Jacobians' : Jacobians, 'Ext_Jacobians' : Extracted_Jacobians, 'Advanced' : Advanced_Metrics, 'DKI': DKI_Metrics,
             'DKI_Thresh' : DKI_Thresh_Metrics, 'MAPMRI' : MAPMRI_Metrics, 'NODDI' : NODDI_Metrics}
Label_Metrics_Dict = {**Basic_Metrics_dict, **Extracted_Metrics_dict, **Native_Metrics_dict, **B0_Removed_Metrics_dict, **Jacobians_Metrics_dict,
                     **DKI_dict, **DKI_Thresh_dict, **MAPMRI_dict, **NODDI_dict}
Advanced_Metrics_Dict = {**DKI_Thresh_dict, **MAPMRI_dict, **NODDI_dict}

Metrics_paradigms = [ "Single_Band" , "Multi_Band" , "Multi_Shell" ]
Extracted_Metrics_paradigms = [ "Single_Shell_Extracted" ]
Native_Metrics_paradigms = [ "Native_Single_Band" , "Native_Multi_Band" , "Native_Multi_Shell" ]
B0_Removed_Metrics_paradigms = [ "Single_Band_B0_Removed" ]
Jacobians_paradigms = [ "Single_Band" , "Multi_Band" , "Multi_Shell" ]
Advanced_Metrics_paradigms = [ "Multi_Shell" ]
DKI_Metrics_paradigms = [ "Multi_Shell" ]
DKI_Thresh_Metrics_paradigms = [ "Multi_Shell" ]
MAPMRI_Metrics_paradigms = [ "Multi_Shell" ]
NODDI_Metrics_paradigms = [ "Multi_Shell" ]

Paradigms_dict = {'Metrics' : Metrics_paradigms, 'Ext_Metrics' : Extracted_Metrics_paradigms, 'Native' : Native_Metrics_paradigms,
                  'B0_Removed' : B0_Removed_Metrics_paradigms, 'Jacobians' : Jacobians_paradigms, 'Advanced' : Advanced_Metrics_paradigms, 'DKI' : DKI_Metrics_paradigms, 'DKI_Thresh' : DKI_Thresh_Metrics_paradigms,
                 'MAPMRI' : MAPMRI_Metrics_paradigms, 'NODDI' : NODDI_Metrics_paradigms}

