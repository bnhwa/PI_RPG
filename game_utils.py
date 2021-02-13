# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 13:00:04 2021

@author: bb339
"""
import os
import sys
import pygame as pg
####################
# File utils
####################
def get_dirs(str_in,prepended = False):

    if prepended:
        return [name for name in os.listdir(str_in+"/") if os.path.isdir(str_in+"/"+name)],str_in
    else:
        dj = os.getcwd()+str_in+"/"
        return [name for name in os.listdir(os.getcwd()+str_in+"/") if os.path.isdir(dj+name)],dj
    
def get_files(str_in,ext, prepended = False, append = False):
    
    # print(os.getcwd()+str_in+"\\")
    ret = []
    retDir =""
    if prepended:
        ret,retDir =  [name for name in os.listdir(str_in+"/") if os.path.isfile(str_in+"/"+name) and ext in name],str_in+"/"
    else:
        dj = os.getcwd()+str_in+"/"
        ret,retDir =  [name for name in os.listdir(os.getcwd()+str_in+"/") if os.path.isdir(dj+name) and ext in name],dj
    if append:
        ret = [dj+"/"+r for r in ret]
    return ret,retDir

####################
# dt utils
####################
def t_convert(item):
    item = item.strip()
    #take string convert to types for setattr
    if item.replace('.', "").isdigit():#cast to float
        return float(item)
    else:#string
        return item
####################
# serial utils
####################
def get_bit(num,pos):
    return num >> pos & 1
if __name__ == '__main__':
    # pg.init()
    # game = Game()
    # game.run()
    # pg.quit()
    pass
####################
# pygame utils
####################
def resize_img(image,cX = None, cY =None):

    oldx, oldy = image.get_rect().size
    if cX is None and cY is None:
        return image
    elif cX is not None and cY is None:
        ratio = (cX/oldx)
        return pg.transform.scale(image, (int(oldx*ratio), int(oldy*ratio)))
    elif cY is not None and cX is None:
        ratio = (cY/oldy)
        return pg.transform.scale(image, (int(oldx*ratio), int(oldy*ratio)))
    else:
        ratioX = (cX/oldx)
        ratioY = (cY/oldy)
        return pg.transform.scale(image, (int(oldx*ratioX), int(oldy*ratioY)))
    return image   