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
from Entity_controller import Entity_controller
        
class Player(Entity_controller):
    def __init__(self):
        self.attacks = []
        
    def set_char(self, entity):
        super(Player, self).__init__("player",entity,self.game)

            
    def update(self):#screen
        global DIFFICULTY
        super().update()
        pressed_keys = pg.key.get_pressed()
        if self.game.game_state<1:
            #continue if dead
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pass
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
                self.attacks+=self.entity.do_attack(self.game, self.id)
            if pressed_keys[pg.K_s]:
                self.attacks+=self.entity.do_attack(self.game, self.id,attack_in="fireball")
            if pressed_keys[pg.K_d]:#and self.entity.onGround:
                if not DIFFICULTY:
                    DIFFICULTY=1

                else:
                    DIFFICULTY=0
            # if pressed_keys[pg.K_s]:
            # self.attacks+=self.entity.do_attack("fireball")   
        #deal with attack objects
        
        self.entity.cooldown-=1
        for a in self.attacks:
            if a.entity.hp<=0 or a.dead:
                self.attacks.remove(a)
            else:
                a.update(self.game.screen)


class Game:
    def __init__(self, _player = Player(), char_start = "jeanne"):
        global glob_player
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.game_entities = {}
        self.game_attacks = {}
        self.game_levels = {}
        self.load_game_entities()
        self.screens = {}
        _player.game = self
        _player.set_char(self.game_entities[char_start])
        self.player = _player
        self.load_levels()
        ####################
        self.load_screens()
        self.font = pg.font.SysFont(None, 20)
        ######################
        self.game_state=0
        self.level = "level_1"

        self.done = False
        self.clock = pg.time.Clock()

    def run(self):
        global DIFFICULTY
        while not self.done:
            self.event_loop()
            if self.game_state ==0:
                #main menu
                self.main_menu("title",reset=1)

            elif self.game_state ==1:
                self.difficulty = DIFFICULTY
                self.game_levels[self.level].update()
                if self.player.entity.state == "dead":    
                    self.game_state=2
            elif self.game_state ==2:
                self.main_menu("game_over")
                self.reset_level()
                DIFFUCLTY=0
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
            


    def main_menu(self,screen_name_use,reset = 0):
        print(screen_name_use)
        global click
        running = True
        while running:
            if USE_ESP:
                self.player.update()
                pass
            self.screen.fill((0,0,0))
            self.screens[screen_name_use].update()
     
            mx, my = pg.mouse.get_pos()     
            click = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    # if event.button == 1:
                    click = True
                    running=False
                    self.game_state=reset
     
            pg.display.update()
            self.clock.tick(FPS)
    def draw_text(self,text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.screen.blit(textobj, textrect)
        
    def load_game_entities(self,verbose = False):
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
        dirs, curr_path = ut.get_dirs("/bin/attacks")
        for i in dirs:
            if verbose :
                print(i)
            ok = curr_path+i+"/"
            print(ok)
            self.game_attacks[i] = moving_entity(i,curr_path+i+"/")    
    
    def load_levels(self,verbose = False):
        #characters
        dirs, curr_path = ut.get_dirs("/bin/levels")
        for i in dirs:
            if verbose :
                print(i)
            ok = curr_path+i+"/"
            print(ok)
            self.game_levels[i] = Level(i,curr_path+i+"/",self)

        pass
    def load_screens(self,verbose = False):
        global game_levels
    
        #screens
        dirs, curr_path = ut.get_dirs("/bin/screens")
        for i in dirs:
            if verbose :
                print(i)
            ok = curr_path+i+"/"
            print(ok)
            # self.game_screens[i] = 
            self.screens[i]=Stills(i,curr_path+i+"/",self)

        pass
class Stills(pg.sprite.Sprite):
    def __init__(self,name,curr_path,game):
        super(Stills, self).__init__()
        self.name=name
        self.game=game
        self.pos  = vec(0,0)
        self.state = "base"
        self.move_frame = 0
        self.state_frames={}
        self.state_inc={}
        self.state_dict={}
        dirs, _ = ut.get_dirs(curr_path+"sprites",prepended=True)
        # print(curr_path)
        # print(dirs)

        for spr in dirs:
            fls, pth =  ut.get_files(curr_path+"sprites/"+spr,".png" ,prepended=True)
            self.state_frames[spr]=len(fls)
            self.state_inc[spr]=float(60/len(fls))/30
            self.state_frames[spr]=len(fls)
            self.state_dict[spr]=[]
            for f in fls:
                #default sprites are oriented to the left
                img_base = pg.image.load(pth+f)
                img_base=ut.resize_img(img_base,cY=screen_height)
                #build right image
                self.state_dict[spr].append(img_base)

        self.image = self.state_dict["base"][0]
    def update(self):
        self.move_frame += self.state_inc[self.state]
        
        if  self.move_frame> self.state_frames[self.state]-1:
            self.move_frame=0
        self.image = self.state_dict[self.state][ int(self.move_frame)]
        self.game.screen.blit(self.image, (self.pos.x, self.pos.y))
if __name__ == '__main__':
    #load entities
    pg.init()
    game = Game()
    game.run()
    pg.quit()
    # print(os.listdir(os.getcwd()+"\\bin\\characters"))