# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 17:47:54 2021

@author: bb339
"""
from Entity import moving_entity
from random import random
from Entity_controller import Entity_controller
from global_vars import *



class Enemies(Entity_controller):
    def __init__(self,entity,game, posX=0,posY=0):
        super(Enemies, self).__init__("enemy",entity,game, posX=0,posY=0)
        #make list of entities

    def update(self):
        # global DIFFICULTY
        # print(DIFFICULTY)
        super().update()
        # self.entity.stop()
        if self.difficulty:
            #if hard, jump towards player
            if self.entity.state not in ["dead","dying"]:
                hdirec,vdirex = 0,0
                if self.entity.pos.x>self.game.player.entity.pos.x:
                    hdirec=-1
                elif self.entity.pos.x<self.game.player.entity.pos.x:
                    hdirec=1
                self.entity.acc.x+=hdirec*self.entity.accel+(self.difficulty*random())
                self.entity.damage = self.difficulty
                if random()<0.5:
                    self.entity.jump()


                
            
            pass
        else:
            if self.entity.state != "dead" and self.entity.onGround:
                direc = 1 if random() >0.5 else -1
                self.entity.pos.x+= direc*self.entity.velocity
            
        
        # self.entity.update(self.game.screen)
        #depending on attack strategy, employ different one
        ###ADD AI
        
        pass
