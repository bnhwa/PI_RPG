# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 19:00:35 2021

@author: bb339
"""

class Entity_controller(object):
    def __init__(self,_id,entity,game,posX=None,posY=None):    
        #make list of entities
        self.id = _id
        self.game = game
        self.entity = entity.copy()
        self.attacks = []
        self.difficulty= 0
        if posX is not None and posY is not None:
            self.entity.set_pos(posX,posY)
        
    def update(self):
        self.difficulty = self.game.difficulty
        self.entity.update(self.game.screen)
        self.entity.stop()
    def reset(self):
        self.entity.reset()
        self.attacks = []
    def rect(self):
        return self.entity.rect
    def set_pos(self,posX,posY):
        self.entity.set_pos(posX,posY)

        
