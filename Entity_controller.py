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
        if posX is not None and posY is not None:
            self.entity.set_pos(posX,posY)
        
    def update(self):
        self.entity.update(self.game.screen)
        self.entity.stop()
    def reset(self):
        self.entity.reset()
    def rect(self):
        return self.entity.rect

        #depending on attack strategy, employ different one
        ###ADD AI
        
        pass
    