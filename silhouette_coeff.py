# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 13:30:00 2020

@author: kic.guest
"""


import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.metrics import silhouette_score
import cv2
from sklearn.preprocessing import scale
from remove_bg import bg_mask
from colorname import color_name
import time



# silhouetteCoeff determination
def silhouetteCoeff(z, mi, ma):
    max_silhouette = 0
    max_k = 0
    if mi < 2:
        mi = 2
        print('The minimum of min_k is 2, ')
        
    if ma < 2 or ma <= mi:
        ma = mi + 2
        print ('max_ k should larger than min_k')
        
    for i in range(mi,ma):
        clt = MiniBatchKMeans(n_clusters = i, random_state = 42)
        clt.fit(z)
        silhouette_avg = silhouette_score(z, clt.labels_, sample_size = 500, random_state = 42)
        #print("k: ", i, " silhouette avg: ", silhouette_avg)
        if (silhouette_avg == 1.0):
            max_k = i
            print("Max k: ", max_k)
            break
        elif (silhouette_avg > max_silhouette):
            max_silhouette = silhouette_avg
            max_k = i
    
    #print("Max silhouette: ", max_silhouette)
    #print("Max k: ", max_k)
    return int(max_k)


# kMeans algorithm
def kMeans(path, mi, ma, seg = False, threshold = 0.25):
        
    # Image preprocessing
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # resize
    while (img.shape[0] > 200 or img.shape[1] > 200):
        img = cv2.resize(img, (int(img.shape[0]*0.75),int(img.shape[1]*0.75)))
        
    #print(img.shape)
    # Remove_background switch
    if seg == False:
        img = cv2.medianBlur(img,11)
        img = img.reshape(-1,3)
    elif seg == True:
        try:
            img = bg_mask(img)
        except IndexError: # For error situation
            img = cv2.medianBlur(img,11)
            img = img.reshape(-1,3)
            seg = False # Turn to segmentation off mode
    
    
    scale_img = scale(img)
    klt = MiniBatchKMeans(n_clusters = silhouetteCoeff(scale_img, mi, ma), random_state = 42)
    klt.fit(img)
    k_centers = klt.cluster_centers_
    #print("k_centers(b): ", k_centers)
    
    
    # Threshold filter (only run in segmentation flag on)
    # Threshold generater or threshold list
    if seg == True:
        label = klt.labels_
        unique, counts = np.unique(label, return_counts=True)
        
        delete=[]
        for idx, x in enumerate(counts):
            if (x/counts.sum()) < threshold :
                delete.append(idx)
        k_centers = np.delete(k_centers,tuple(delete),0)
        if k_centers.shape[0] == 0:
            k_centers = kMeans(path, mi, ma, False) ## recursion with segmentation flag off
    
    return k_centers.astype('int')



if __name__ == '__main__':
    
    ## for testing only
    t0 = time.time()
    path = 'image/cloth1.jpg'
    x = kMeans(path, 2, 8, seg = False, threshold=0.2)
    print(color_name(x))
    print(f'Time:{time.time()-t0}')