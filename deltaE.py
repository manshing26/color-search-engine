 # -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 13:52:57 2020

@author: kic.guest
"""

from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000
import time
from skimage.color import rgb2lab
import numpy as np


def de2000(rgb1, rgb2, de = 5):
    '''
    

    Parameters
    ----------
    rgb1 : TYPE List, len_of_list = 3
        For example, rgb1 = [0,0,255]
        
    rgb2 : TYPE List, len_of_list = 3
        Refer to rgb1
        
    de : TYPE interger, optional
        DESCRIPTION. The default is 10.

    Returns
    -------
    bool
        DESCRIPTION.

    '''
    rgb1 = [[rgb1]]
    rgb2 = [[rgb2]]
    
    np1 = np.asarray(rgb1)/255
    np2 = np.asarray(rgb2)/255
    
    lab1 = rgb2lab(np1)[0][0]
    lab2 = rgb2lab(np2)[0][0]
    
    color1 = LabColor(lab1[0], lab1[1], lab1[2])
    color2 = LabColor(lab2[0], lab2[1], lab2[2])
    
    delta_e = delta_e_cie2000(color1, color2)
    #print(f"Color difference: {delta_e}")
    
    if delta_e <= de:
        return True, delta_e
    else:
        return False, delta_e
    
    
# For testing
if __name__ == "__main__":
    t0 = time.time()

    # Maximum of color difference ==> 100 (black vs white)
    rgb1 = [0,0,0]
    rgb2 = [255,255,255]
    
    _,Answer = de2000(rgb1, rgb2)
    print(f"Running time: {time.time()-t0}")
    print(Answer)