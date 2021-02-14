# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 16:21:46 2021

@author: bb339
"""


from global_vars import *
import os
import pygame as pg
import game_utils as ut
from random import random
from Entity import Entity,moving_entity
from Enemies import Enemies

#################################
# Level, bg & terrain
#################################
class Level(object):
    def __init__(self, name, curr_path,game):
        self.game = game
        self.player = game.player
        self.screen = game.screen
        self.x = 1;
        self.curr_path = curr_path
        self.bg =Background(curr_path)
        self.terrain =Background(curr_path,name = "terrain.png")
        self.collidebg=pg.sprite.Group(self.terrain)
        self.mov_entities = []
        self.alive_enemies = []
        self.curr_moving = []
        self.enemies = []
        self.attacks = []
        self.load_entities()
        ###
        self.diff_level = 3
        self.entity_limit = 15
        ###
        # self.reset()
        
        
    def load_entities(self, reset = False):
        # print("asdfasdfsadfa")
        # print(glob_player)
        #load entities, set each to alive
        attr_fl = open(self.curr_path+"placement.txt", "r")
        attr_list = list(map(lambda x: [x[0],           list(map(lambda y: ut.t_convert(y),x[1].strip().split(",")) )],\
                    [i.split("=") for i in attr_fl.read().replace(' ', "")\
                        .split("\n") if i.strip() != ""]))
        attr_fl.close()
        if not reset:
            self.mov_entities=[]
            for k,v in attr_list:
                if k == "player":
                    self.player.entity.set_pos(v[0],v[1])
                    self.mov_entities.append(self.player)
                else:
                    self.add_entity(k,v[0],v[1])

                    
        else:
            for m,v in zip(self.mov_entities,list(map(lambda x: x[1],attr_list))):
                # print(v)
                m.set_pos(v[0],v[1])
                m.reset()
        self.curr_moving+=self.mov_entities

    def add_entity(self,entity_name,posX = None,posY =None,set_pos=False):
        if posX is None:
            posX = screen_width/2+      ( [-1,1][round(random())])*(screen_width/4)
        if posY is None:
            posY = random()*screen_height
        tmp = Enemies(self.game.game_entities[entity_name],self.game,posX=posX,posY=posY)
        if (posX is not None and posY is not None) or set_pos:
            tmp.set_pos(posX,posY)
        self.enemies.append(tmp)
        # self.alive_enemies.append(tmp)
        self.mov_entities.append(tmp)
        self.curr_moving+=[tmp]
        
    def reset(self):
        #reset entities and their positions
        # Loading screen?
        self.diff_level = 3
        self.enemies = []
        self.curr_moving = []
        self.attacks = []
        self.load_entities(reset=False)
        

    def update(self):
        global DIFFICULTY
        ##########################
        self.bg.update(self.screen)
        self.terrain.update(self.screen)
        #player
        ###########################
        # Collision Checking
        ###########################
        #--------------------------
        #apply gravity and terrain check
        #--------------------------
        for m in self.curr_moving:
            if m.entity.state != "dead":
                m.entity.acc.y=+3;
                self.terrain_check(m.entity)
                m.update()
            else:
                #clean out "dead" entities for sake pf processing
                self.curr_moving.remove(m)

        # print(len(self.curr_moving))
        for m in self.mov_entities:
            m.entity.render(self.screen)
        #--------------------------
        #attack collision: Player attacks to enemies
        #--------------------------
        for a in self.player.attacks:#get all entity attacks
            for m in self.curr_moving:
                # attacks "all" damage all, else, "player" attacks wont damage player
                if a.attack_id != m.id and a.entity.rect.colliderect(m.rect()):
                    # print(a.attack_id, m.id)
                    m.entity.hp-=a.entity.damage
        #             a.dead = True
        #--------------------------
        #attack collision: all friendly-fire attacks 
        #--------------------------
        # for a in self.player.attacks:#get all entity attacks
        #     for m in self.curr_moving:
        #         # attacks "all" damage all, else, "player" attacks wont damage player
        #         if a.attack_id != m.id and a.entity.rect.colliderect(m.entity.rect):
        #             m.entity.hp-=a.entity.damage
        #             a.dead = True
                
            # .colliderect(m.entity.rect)
        
        #--------------------------
        # entity - entity collision
        #--------------------------
        # self.alive_enemies
        for m in self.curr_moving:
            if self.collision_entities(m,self.player):
                self.player.entity.hp-=m.entity.damage
        if len(self.curr_moving)==1 and len(self.mov_entities)<self.entity_limit*2:
            self.diff_level+=1
            for i in range(self.diff_level):
                self.add_entity("slime",set_pos=True)
            if (self.diff_level % 2)==0:
                DIFFICULTY+=1
            
        
        
    def terrain_check(self,moving_ent):
        """
        naive collision handling with background sprite
        """
        global screen_width
        #apply gravity if no collision
        # if moving_ent.
        if moving_ent.rect.center[0]<=0:
            moving_ent.pos.x=screen_width#-moving_ent.rect.size[0]
        elif moving_ent.rect.center[0]>screen_width:
            moving_ent.pos.x=0#int(moving_ent.rect.size[0]/2)
        hits = pg.sprite.spritecollide(moving_ent, pg.sprite.Group(self.terrain), False, pg.sprite.collide_mask)
        if hits:
            moving_ent.vel.y = 0
            moving_ent.acc.y = 0
            moving_ent.jumping = False
            moving_ent.onGround = True
            if moving_ent.hp<=0 and moving_ent.state == "dying":
                # moving_ent.dead = True
                moving_ent.state = "dead"
            # moving_ent.pos.y+=5
        else:
            moving_ent.onGround = False
            moving_ent.state="jumping"

    def rect_check(self,moving_ent):
        """
        collision handling with individual rect platforms with anti-clipping
        """
        #collision handling with individual platforms
        #apply gravity if no collision
        hits = pg.sprite.spritecollide(moving_ent, pg.sprite.Group(self.terrain), False, pg.sprite.collide_mask)
        if hits:
            #only for individual rectangles
            if moving_ent.pos.y < lowest.rect.bottom:
                moving_ent.pos.y = lowest.rect.top + 1
                moving_ent.vel.y = 0
                moving_ent.acc.y = 0
                moving_ent.jumping = False
                
    def basic_check(self,moving_ent):
        if moving_ent.pos.y >= screen_height-50: 
            moving_ent.vel.y = 0
            moving_ent.acc.y = 0
            moving_ent.jumping = False
            moving_ent.pos.y=screen_height-50
            moving_ent.onGround = True
            if moving_ent.hp<=0: moving_ent.state = "dead"
            
    def collision_entities(self,control1,control2):
        #collision between entities
        if control1.id == control2.id :return False
        hits = pg.sprite.spritecollide(control1.entity, pg.sprite.Group(control2.entity), False, pg.sprite.collide_mask)
        if hits:
            return True
        else:
            return False
        #collide one by one
        # pg.sprite.spritecollide(self.player.entity, self.enemies, False, pg.sprite.collide_mask)
        
        pass
    
class Background(pg.sprite.Sprite):
    def __init__(self,curr_path,name = None):
        super(Background, self).__init__()
        self.pos  = vec(0,0)
        if name is None:
            self.image = pg.image.load(curr_path+"background.png")
        else:
            self.image = pg.image.load(curr_path+name)
        self.image = ut.resize_img(self.image,cY=screen_height)
        self.rect = self.image.get_rect(center=(int(screen_width/2),int(screen_height/2)))
        self.mask = pg.mask.from_surface(self.image)
        # print(self.rect.size)

 
    def update(self,screen):
        screen.blit(self.image, (self.pos.x, self.pos.y))