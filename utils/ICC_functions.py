#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd


def mask_data(data):
    
    ####Pass data as a list
    tmp = np.stack(data, axis=2)
    mask = np.any(np.isnan(tmp), axis=(1,2))
    return mask

def Add_To_Dataframe(Data, Paradigms, Metrics, ROIS, df, GDT=True):
    X = Data.shape
    if GDT==True:
        GDT_stat=1
    else:
        GDT_stat=0       
    for Paradigm_index, Paradigm in enumerate(Paradigms):
        for Metric_index, Metric in enumerate(Metrics):
            for ROI_index, ROI in enumerate(ROIS):
                ndf = pd.DataFrame( { "Paradigm" : Paradigms[Paradigm_index], "Metric" : Metrics[Metric_index], "ROI" : ROIS[ROI_index], 
                           "Value" : Data[ROI_index, Metric_index, Paradigm_index], "GDT" : GDT_stat }, index = [0])
                df=pd.concat([df,ndf])
        
    df=df.set_index(np.arange(df.shape[0]))
    return df



def load_images(Reg_files, GDT_files):
    #Initialize 5-D array
    reg_concat_image = np.zeros((256,256,150, num_subjects, num_sessions))
    GDT_concat_image = np.zeros((256,256,150, num_subjects, num_sessions))
    for i in range(0,num_subjects):
        for j in range(0,num_sessions):

            print("subject: ", i+1)
            print("session: ", j+1)

            if os.path.isfile(Regular_files_array[i,j]):
                reg_concat_image[:,:,:,i,j]=nipy.load_image(Regular_files_array[i,j]).get_data()
            else:
                print("no File")
                reg_concat_image[:,:,:,i,j]=np.nan

            if os.path.isfile(GDT_files_array[i,j]):
                GDT_concat_image[:,:,:,i,j]=nipy.load_image(GDT_files_array[i,j]).get_data()
            else:
                print("no File")
                GDT_concat_image[:,:,:,i,j]=np.nan 
                
    return (reg_concat_image, GDT_concat_image)



def ICC_Voxelwise_Vector(data,mask):
    
    """Pass mask as a boolean np array
    """
    
    ##########################################################
    #Need to add in to drop image if any session is all nans!#
    ##########################################################
    
    # 30*3 list of images which are all NaNs
    Image_Nans = np.all(np.isnan(data[mask]), axis=0)
    
    # 30*1 list of subjects for which any session is all NaNs
    Session_Nans = Image_Nans.any(axis=1)
    
    # Mask data to remove rows with NaN sessions
    data = data[:,:,:,~Session_Nans,:]
    
    #Drop negatives
    data=np.absolute(data)
    
    ##Shape of input data
    datshape = data.shape
    

    ##########################################################
    # ICC CALCULATION
    ##########################################################
    
    grandmeans = np.zeros([datshape[0],datshape[1],datshape[2]])
    Subject_Means = np.zeros([datshape[0],datshape[1], datshape[2], datshape[3]])
    Session_Means = np.zeros([datshape[0],datshape[1], datshape[2], datshape[4]])

    grandmeans[mask]=np.mean(data[mask])

    Subject_Means[mask] = np.mean(data[mask], axis=2)
    Session_Means[mask] = np.mean(data[mask], axis=1)
    grandmeans[mask] = np.mean(data[mask],axis=(1,2))


    #INIT vars

    BMS = np.zeros([datshape[0],datshape[1],datshape[2]])
    WMS = np.zeros([datshape[0],datshape[1],datshape[2]])
    JMS = np.zeros([datshape[0],datshape[1],datshape[2]])
    EMS = np.zeros([datshape[0],datshape[1],datshape[2]])
    SST = np.zeros([datshape[0],datshape[1],datshape[2]])
    PMS = np.zeros([datshape[0],datshape[1],datshape[2]])
    sv=np.zeros(datshape[1])


    ##Loops over Subject
    BMS[mask] = ((Subject_Means[mask] - grandmeans[mask,None])**2).sum(axis=1)
    
    #Loops over Subject then Session
    WMS[mask] = ((data[mask] - Subject_Means[mask,:,None])**2).sum(axis=(1,2))
    EMS[mask] = ((data[mask] - Subject_Means[mask,:,None] - Session_Means[mask,None,:] + grandmeans[mask,None,None])**2).sum(axis=(1,2))
    SST[mask] = ((data[mask] - grandmeans[mask,None,None])**2).sum(axis=(1,2))
    
    #Loops over Session
    JMS[mask] = ((Session_Means[mask] - grandmeans[mask,None])**2).sum(axis=1)
    
    #Loops over Session then Subject
    PMS[mask] = ((data[mask] - Session_Means[mask,None,:])**2).sum(axis=(1,2))

            #        sv[j] = sv[j] + (data[i,j] - Session_Means[j])**2          

    nsubjects=datshape[3]
    nsessions=datshape[4]

    #Correct

    BMS[mask] = nsessions*BMS[mask]/(nsubjects-1);
    WMS[mask] = WMS[mask]/(nsessions-1)/nsubjects;
    JMS[mask] = nsubjects*JMS[mask]/(nsessions-1);
    EMS[mask] = EMS[mask]/(nsessions-1)/(nsubjects-1); 
    PMS[mask] = PMS[mask]/(nsessions-1)/(nsubjects-1); 
    #Here we are dividing by zero
    ICC = (BMS - EMS) / (BMS + (nsessions-1)*EMS)
    CVws = (WMS ** 0.5) / grandmeans;
    CVbs = (BMS ** 0.5) / grandmeans;
    #Here we are dividing by zero
    print(np.any(np.isnan(BMS)))
    print(np.any(np.nonzero(BMS)))


    #return( BMS, WMS, JMS, EMS, PMS, Subject_Means, Session_Means)
    return (ICC, CVws, CVbs)   

def ICC(data, mask=None):
    
    ####Make mask if none passed
    if mask is None:
        mask = np.any(np.isnan(data), axis=1)

    ####Drop rows if any nans
    if np.any(mask) == True:
        data = data[~mask]
    
    #Drop negatives
    data=np.absolute(data)
    
    ICC = 0
    CVws = 0
    CVbs = 0
    
    #Calculating various means
    grandmean = np.mean(data)
    Session_Means=np.mean(data, axis=0)
    Subject_Means=np.mean(data, axis=1)

    #INIT vars
    BMS=0; WMS=0; JMS=0; EMS=0;
    SST=0; PMS=0
    sv=np.zeros(data.shape[1])

    nsubjects=data.shape[0]
    nsessions=data.shape[1]

    
    #Calculate Mean Squares
    for i in range (0, data.shape[0]):
        BMS = BMS + (Subject_Means[i]-grandmean)**2

        for j in range (0, data.shape[1]):
            WMS = WMS + (data[i,j]-Subject_Means[i])**2

            EMS = EMS + (data[i,j] - Subject_Means[i] - Session_Means[j] + grandmean)**2
            SST = SST + (data[i,j] - grandmean)**2

    for j in range(0,data.shape[1]):
        JMS = JMS + (Session_Means[j] - grandmean)**2


    for j in range(0,data.shape[1]):
        for i in range(0,data.shape[0]):
            PMS = PMS + (data[i,j] - Session_Means[j])**2
            sv[j] = sv[j] + (data[i,j] - Session_Means[j])**2            

    #Correct
    BMS = nsessions*BMS/(nsubjects-1);
    WMS = WMS/(nsessions-1)/nsubjects;
    JMS = nsubjects*JMS/(nsessions-1);
    EMS = EMS/(nsessions-1)/(nsubjects-1); 
    PMS = PMS/(nsessions-1)/(nsubjects-1); 

    ICC = (BMS - EMS) / (BMS + (nsessions-1)*EMS)
    CVws = (WMS ** 0.5) / grandmean;
    CVbs = (BMS ** 0.5) / grandmean;
    
    return (ICC, CVws, CVbs)

