# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 12:30:07 2021

@author: bb339
"""
#uses tkinter
# pip install tk
from tkinter import * 
from tkinter.ttk import *
import pickle
import pygame as pg
import os
import sys
import game_utils as ut
from global_vars import *
from Entity import Entity,moving_entity
from Level import Level, Background
        
        
class Player(object):
    def __init__(self):
        self.attacks = []
        
    def set_char(self, entity):
        self.entity = entity.copy()
        #make list of entities
            
    def update(self,screen):#screen
        self.entity.update(screen)
        self.entity.stop()
        pressed_keys = pg.key.get_pressed()

        if self.entity.hp>0: 
            if pressed_keys[pg.K_LEFT]:
    
                self.entity.acc.x = -self.entity.accel
            if pressed_keys[pg.K_RIGHT]:
                self.entity.acc.x = self.entity.accel#ACC 
                
            if pressed_keys[pg.K_DOWN]:#and self.entity.onGround:
                self.entity.crouch()
        
            if pressed_keys[pg.K_SPACE]:
                self.entity.jump()
                
            if pressed_keys[pg.K_a]:
                self.attacks+=self.entity.do_attack(self.game)
            if pressed_keys[pg.K_s]:
                self.attacks+=self.entity.do_attack(self.game,"fireball")
            # if pressed_keys[pg.K_s]:
            # self.attacks+=self.entity.do_attack("fireball")   
        #deal with attack objects
        
        self.entity.cooldown-=1
        for a in self.attacks:
            if a.entity.hp<=0 or a.dead:
                self.attacks.remove(a)
            else:
                a.update(screen)


class Game:
    def __init__(self, _player = Player(), char_start = "jeanne"):
        global glob_player
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.game_entities = {}
        # self.game_enemies = {}
        self.game_attacks = {}
        self.game_levels = {}
        self.load_game_entities()
        _player.set_char(self.game_entities[char_start])
        
        glob_player = _player
        self.player = _player
        self.player.game = self
        self.load_levels()
        
        self.game_state=1
        self.level = "level_1"

        self.done = False
        self.clock = pg.time.Clock()

    def run(self):
        while not self.done:
            self.event_loop()
            
            self.game_levels[self.level].update()
            # self.update()
            pg.display.flip()
            #set fps pi 30 fps bc Raspberry pi is a potato
            self.clock.tick(FPS)
                  
            
            #self.clock.tick(60)
    def reset_level(self,level = None):
        # self.resetting = True
        level = self.level if level is None else level
        self.game_levels[level].reset()
        # self.resetting = False
        
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
        pressed_keys = pg.key.get_pressed()
        
        
        if pressed_keys[pg.K_r]:
            self.reset_level()
            


    def main_menu(self):
        pass

    def load_game_entities(self,verbose = False):
        global game_entities
        char_dir = "/bin/characters"
        #characters
        dirs, curr_path = ut.get_dirs("/bin/characters")
        for i in dirs:
            if verbose :
                print(i)
            ok = curr_path+i+"/"
            print(ok)
            # print(os.listdir(ok))
            self.game_entities[i] = moving_entity(i,curr_path+i+"/")

        #enemies
        dirs, curr_path = ut.get_dirs("/bin/enemies")
        for i in dirs:
            if verbose :
                print(i)
            ok = curr_path+i+"/"
            print(ok)
            self.game_entities[i] = moving_entity(i,curr_path+i+"/")
            # self.game_enemies[i] = moving_entity(i,curr_path+i+"/")
        dirs, curr_path = ut.get_dirs("/bin/attacks")
        for i in dirs:
            if verbose :
                print(i)
            ok = curr_path+i+"/"
            print(ok)
            self.game_attacks[i] = moving_entity(i,curr_path+i+"/")    
    
    def load_levels(self,verbose = False):
        global game_levels
        char_dir = "/bin/levels"
    
        #characters
        dirs, curr_path = ut.get_dirs("/bin/levels")
        for i in dirs:
            if verbose :
                print(i)
            ok = curr_path+i+"/"
            print(ok)
            self.game_levels[i] = Level(i,curr_path+i+"/",self)

        pass


if __name__ == '__main__':
    #load entities
    pg.init()
    game = Game()
    game.run()
    pg.quit()
    # print(os.listdir(os.getcwd()+"\\bin\\characters"))