# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:28:23 2020

@author: kic.guest

This module is used for return the color name of image
"""


import color_dir as cd

def nearColor(requested_colour):
    min_colours = {}
    #for key, name in wc.css3_hex_to_names.items():
    for key in cd.rgb_to_name_dict:
        #r_c, g_c, b_c = wc.hex_to_rgb(key)
        r_c, g_c, b_c = key
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = cd.rgb_to_name_dict[key]
    return min_colours[min(min_colours.keys())]

    
def color_name(color_list):
    color_name_list = []
    
    for idx in range(len(color_list)):
        add = nearColor(color_list[idx])
        if add not in color_name_list:
            color_name_list.append(add)
    
    return color_name_list
