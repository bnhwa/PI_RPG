# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 12:28:29 2021

@author: bb339
"""

from tkinter import * 
from tkinter.ttk import *
import pygame as pg

# glob_player = None
#player characters
# game_entities = {}
# #enemies
# game_enemies = {}
# #levels
# game_levels = {}
# game_attacks = {}
# #screenx screeny
root = Tk() 
screen_height = root.winfo_screenheight() 
screen_width = root.winfo_screenwidth()
#screen_height,screen_width = int(screen_height/2),int(screen_width/2)
print(screen_width,screen_height)
##
vec = pg.math.Vector2
FRIC = -0.10
FPS =60
USE_ESP=1