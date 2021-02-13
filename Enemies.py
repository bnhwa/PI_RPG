# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 17:47:54 2021

@author: bb339
"""
from Entity import moving_entity
from random import random

from global_vars import *



class Enemies(moving_entity):
    def __init__(self,entity,game, posX=0,posY=0):    
        #make list of entities
        self.game = game
        self.entity = entity.copy()
        self.entity.set_pos(posX,posY)
    def update(self):
        
        self.entity.stop()
        
        if self.entity.state != "dead" and self.entity.onGround:
            direc = 1 if random() >0.5 else -1
            self.entity.pos.x+= direc*self.entity.velocity
        
        
        self.entity.update(self.game.screen)
        #depending on attack strategy, employ different one
        ###ADD AI
        
        pass
    