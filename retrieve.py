# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 13:30:42 2020

@author: kic.guest
"""

import click
import pandas as pd
from silhouette_coeff import kMeans
from deltaE import de2000
from save_csv_2 import savefunction


@click.command()
@click.option('-i', '--image', required = True)
@click.option('-d','--dire', required=True)
@click.option('--de', default=3) # default DeltaE ==> 3
def cli(image, dire, de):
    retrieve_result(image, dire, de)


def retrieve_result(image, dire, de):
    # Extract the rgb value of input image
    print('\nExtracting RGB value...')
    result = kMeans(image,2,8)
    print(result)
    
    # Read csv file, if csv file not exist, create a new one
    csv_file = dire+'dataframe.csv'
    print('\nComparing to database...')
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("\ndataframe.csv file not found, generating new .csv file...")
        savefunction(dire,2,8)
        df = pd.read_csv(csv_file)
        
    # Compare the rgb value by DeltaE
    retrieve = {}
    for index, row in df.iterrows():
        color = [row['R'],row['G'],row['B']]
        for e_color in result:
            answer = de2000(color, e_color, de)
            if answer[0] and row['Image'] not in retrieve: # answer[0] --> True/False
                retrieve[row['Image']] = answer[1]
                break
            
    retrieve = sorted(retrieve.items(), key=lambda x: x[1]) # Change to list of tuple
    
    # print result
    print(f'\nImages of similar color (DeltaE = {de}):')
    for f_name in retrieve:
        print(f'{f_name[0]}: DeltaE = {f_name[1]}')
    print(f'\nNumber of result: {len(retrieve)}')
    
    return retrieve
                

if __name__ == "__main__":
    cli()