# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 11:41:18 2020

@author: kic.guest
"""


import cv2
import numpy as np
import numpy.ma as ma
import time


def bg_mask(img, CANNY_THRESH_1 = 10, CANNY_THRESH_2 = 50, MASK_ITER = 10, BLUR = 5,
              save = False, save_path = 'remove_bg.png'):
    
    # Read image in GRAY format
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(3,3),0)
    
    # Edge detection
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2) # Test in image size 350*350

    # Noise removing
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)
    
    # Find contour and find the largest area (background)
    contour_info = []
    try:
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    except ValueError:
        _, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
            ))

    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]
    
    # Create mask and fill it
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255)) ## 255 --> color we want
    
    # Smooth the mask
    mask = cv2.dilate(mask, None, iterations=MASK_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ITER)
    ##mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    
    # Drop the masked area
    drop_list = []
    for idx, x in enumerate(mask.reshape(-1)):
        if x == 0: 
            drop_list.append(idx)
    
    blur = cv2.medianBlur(img,11)
    img_drop = np.delete(blur.reshape(-1,3),drop_list,axis=0)
    
    
    if save:
        # Make the background transparent
        img = img.astype('float32') / 255.0
        b, g, r = cv2.split(img)
        img_print = cv2.merge((b, g, r, mask.astype('float32') / 255.0))
        cv2.imwrite(save_path, img_print*255)
    
    return(img_drop)

# Test
if __name__ == "__main__":
    t0 = time.time()
    img = cv2.imread('image/yarn3.jpg')
    t_img = bg_mask(img,save=True,save_path='image/yarn3_NoBG.png')
    print(f"Time = {time.time()-t0}")