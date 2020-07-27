#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec


def mask_data(data, mask):
    data[~mask] = 0
    data[data==0]=np.nan
    
    return data

def unpad_data(data, paddings=[[55,55],[35,45],[0,0]]):
    #Padding by 1 then adding to paddings accounts for case where padding=0
    data = np.pad(data, ((1,1),(1,1),(1,1)), mode='constant')
    paddings = [ [item1+1, item2+1] for item1, item2 in paddings ]
    
    data = data[paddings[0][0]:-paddings[0][1], paddings[1][0]:-paddings[1][1], paddings[2][0]:-paddings[2][1]]
    return data

def get_quads(blankspace='top_right'):
    
    if blankspace=='top_right':
        return [0,2,3,1]
    if blankspace=='top_left':
        return [1,2,3,0]
    if blankspace=='bottom_right':
        return [0,1,2,3]
    if blankspace=='bottom_left':
        return [0,1,3,2]

def quadrant_plot(data, astr, pos=[110,50,60], blankspace='top_right', cmap='hot'):
    fig = plt.figure(figsize=(5,10), dpi=100)
    
    quads = get_quads(blankspace=blankspace)

    gs  = gridspec.GridSpec(4,2, height_ratios=[1, 1 ,1, 1.5])    
    ax0 = plt.subplot(gs[quads[0]])
    ax1 = plt.subplot(gs[quads[1]])
    ax2 = plt.subplot(gs[quads[2]])
    
    ax3 = plt.subplot(gs[quads[3]])
    ax3.axis('off')
    plt.annotate(astr, (0.2, 0.4),xycoords='axes fraction', fontsize=16)
    
    plt.subplots_adjust(hspace=0.01)
    ax0.imshow((data[pos[0],:,:].T[::-1]),cmap=cmap)
    ax0.axis('off')
    ax1.imshow((data[:,pos[1],:].T[::-1]),cmap=cmap)
    ax1.axis('off')
    ax2.imshow((data[:,:,pos[2]]),cmap=cmap)
    ax2.axis('off')

    plt.show()
