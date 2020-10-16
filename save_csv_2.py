# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 14:29:56 2020

output the .csv file of RGB value

@author: kic.guest
"""


import glob
import os
import click
from silhouette_coeff import kMeans
import pandas as pd
import numpy as np
import time
from tqdm import tqdm


# Click option
@click.command()
@click.option('-p', '--path', required=True)
@click.option('-mi','--min_k', default=2, help='The min_k, minimum is 2, default is 2')
@click.option('-ma','--max_k', default=8, help='The max_k, default is 8')
def cli(path, min_k, max_k):
    '''Read the image by path and return RGB value'''
    savefunction(path,min_k,max_k)

def savefunction(path,min_k,max_k):
    temp_name = 'temp.csv'
    df_name = 'dataframe.csv'
    
    file_list = glob.glob(os.path.join(path, '*.jpg'))
    file_list_checked,exist = check_marker(file_list, path)
    
    df = pd.DataFrame
    flag = file_list_checked[0].split('\\')[-1]
    try:
        if exist: # temp.txt exist
            df = pd.read_csv(path+temp_name)
            df = df.drop(['Unnamed: 0'],axis=1)
        else:
            df = pd.DataFrame({'Image':[], 'R':[],'G':[],'B':[]})
        
        print('\nStart extracting RGB value...')
        t0 = time.time()
        speed_count = 0
        
        for filename in tqdm(file_list_checked):
            result = kMeans(filename, min_k, max_k)
            name = filename.split('\\')
            names = np.asarray([[name[-1]]]*result.shape[0])
            add = np.append(names, result, axis=1)
            df = df.append(pd.DataFrame(add, columns=['Image','R','G','B']), ignore_index=True)
            flag = name[-1]
            speed_count += 1
    except:
        with open((path+'temp.txt'),'w+') as f:
            f.write(flag)
        print('\nExtraction aborted, .csv file and temp.txt exported')
    finally:
        if df.empty != True:
            save_path = path+temp_name
            df.to_csv(save_path, header=True)
            
        if flag == file_list[-1].split('\\')[-1]:
            save_path = path+df_name
            df.to_csv(save_path, header=True)
            os.remove((path+'temp.txt'))
            os.remove((path+temp_name))
            
            
            print('\nExtraction completed, .csv file exported')
            
        print(df)
        if speed_count != 0:
            print(f'Speed: {(time.time()-t0)/speed_count}s for each image')

def check_marker(file_list, path):
    exist = False
    try:
        with open((path+'temp.txt'),'r') as f:
            marker = f.read()
    
        search = (path+marker).replace('/','\\')
        if search in file_list:
            print('\nRecord matched')
            exist = True
            idx = file_list.index(search)+1 # Flag is already finished KMeans, so +1
            return file_list[idx:], exist
        else:
            print('\ncannot match with previous record')
            return file_list, exist
    except:
        print('\ntemp.txt not found, extraction start from zero')
        return file_list,False
    
    
if __name__ == '__main__':
    cli()