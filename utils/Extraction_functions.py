#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from nipype.interfaces.fsl import ImageStats
from nipype.testing import funcfile
import os, fnmatch


def FSLROI_Image(Image, ROI):
    """Performs fslstats to extract values from Image at location denoted
        by ROI."""
    stats = ImageStats(in_file=Image, op_string='-k %s -m' %ROI)
    return(stats.aggregate_outputs().out_stat)

def find(pattern, path, fullpath=True):
    """returns paths in path which match pattern"""
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                if fullpath==True:
                    result.append(os.path.join(root, name))
                else:
                    result.append(name)
    return result