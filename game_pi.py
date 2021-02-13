# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 12:30:07 2021

@author: bb339
"""
#uses tkinter
# pip install tk
from tkinter import * 
from tkinter.ttk import *
import pygame as pg
import os
import sys
import game_utils as ut
from global_vars import *
from game import Game

import serial

##globals
fl_ = open("settings.txt","r")
SERIAL_PORT = fl_.read().strip()
fl_.close()
USE_ESP = 1
CONTROL_VAL = 128
baudrate = 9600
currVal = 128

ser = serial.Serial(SERIAL_PORT,baudrate,timeout=0.0001)

        
class Player(object):
    def __init__(self):
        self.attacks = []
        
    def set_char(self, entity):
        self.entity = entity.copy()
        
        
    def update(self,screen):#screen
        self.entity.update(screen)
        self.entity.stop()
        self.entity.cooldown-=1
        pressed_keys = pg.key.get_pressed()
        if USE_ESP:
            
            left_right = ut.get_bit(CONTROL_VAL,0)
            lr_move = ut.get_bit(CONTROL_VAL,1)
            up_down = ut.get_bit(CONTROL_VAL,2)
            ud_move = ut.get_bit(CONTROL_VAL,3)
            blue = ut.get_bit(CONTROL_VAL,4)
            red = ut.get_bit(CONTROL_VAL,5)
            spell = ut.get_bit(CONTROL_VAL,6)
            # print("v_yn:{},vm:{},h_yn:{},hm:{}".format(ud_move,up_down,lr_move,left_right))  
            if self.entity.hp>0: 
                if lr_move:
                    if left_right:#not
                        self.entity.acc.x = -self.entity.accel
                    else:
                        self.entity.acc.x = self.entity.accel#ACC 
                if ud_move:
                    if  up_down:#not
                        self.entity.jump()
                    else:
                        self.entity.crouch()
                if blue:
                    self.attacks+=self.entity.do_attack(self.game,"fireball")         
                if red:
                    self.attacks+=self.entity.do_attack(self.game)   
        else:
            if self.entity.hp>0: 
                if pressed_keys[pg.K_LEFT]:
        
                    self.entity.acc.x = -self.entity.accel
                if pressed_keys[pg.K_RIGHT]:
                    self.entity.acc.x = self.entity.accel#ACC 
                    
                # if pressed_keys[pg.K_DOWN]:
                #     self.state="crouch"
                if pressed_keys[pg.K_SPACE]:
                    self.entity.jump()
                    
                if pressed_keys[pg.K_a]:
                    self.attacks+=self.entity.do_attack()    
                if pressed_keys[pg.K_s]:
                    self.attacks+=self.entity.do_attack("fireball")           
        #deal with attack objects   
        for a in self.attacks:
            if a.entity.hp<=0 or a.dead:
                self.attacks.remove(a)
            else:
                a.update(self.game.screen)
        
        # if pressed_keys[pg.K_r]:
        #     self.entity.reset()
                





################################################################
#serial
################################################################

    
def get_serial():
    global CONTROL_VAL
    data = ser.read(1)
    data+= ser.read(ser.inWaiting())
    if len(data) == 5:
        CONTROL_VAL = int(data[:3])


            
if __name__ == '__main__':

    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    pg.init()
    game = Game(_player=Player())
    game.run()
    pg.quit()


    
    # print(os.listdir(os.getcwd()+"\\bin\\characters"))