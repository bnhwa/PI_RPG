# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 12:28:29 2021

@author: bb339
"""

from tkinter import * 
from tkinter.ttk import *
import pygame as pg
import game_utils as ut
import os

fl_ = open("settings.txt","r")
settings_dict = {i[0]:ut.t_convert(i[1]) for i in list(map( lambda x:x.split("="), fl_.read().replace(" ","").split("\n")   ))}
fl_.close()
root = Tk()
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
screen_setting = settings_dict["fullscreen"]
OFFSET = 1
if  screen_setting==0:
    screen_height = 864
    screen_width = 1536
elif screen_setting==2:
    screen_height = int(root.winfo_screenheight()/2)
    screen_width = int(root.winfo_screenwidth()/2)
    OFFSET = (screen_width/1536)*1.5
    print(OFFSET)
#screen_height,screen_width = int(screen_height/2),int(screen_width/2)
print(screen_width,screen_height)
##
vec = pg.math.Vector2
FRIC = -0.10
FPS =60
USE_ESP=1
DIFFICULTY=1