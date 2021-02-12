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

import serial

##globals
SERIAL_PORT = "COM3"
USE_ESP = 1
CONTROL_VAL = 128
port = "COM3"
baudrate = 9600
currVal = 128

ser = serial.Serial(port,baudrate,timeout=0.0001)

# CONTROL_VAL = multiprocess.Value('i',0)
#


#GAME
glob_player = None
#player characters
game_entities = {}
#enemies
game_enemies = {}
#levels
game_levels = {}
game_attacks = {}
#screenx screeny
root = Tk() 
screen_height = root.winfo_screenheight() 
screen_width = root.winfo_screenwidth()
#screen_height,screen_width = int(screen_height/2),int(screen_width/2)
print(screen_width,screen_height)
##
vec = pg.math.Vector2
FRIC = -0.10
FPS = 30
#################################
# Entities
#################################

class Entity(pg.sprite.Sprite):
    
    def __init__(self, name, curr_path,scale = None,verbose = False,copy_vals = None):
        """
        Entity class, uses copy_vals and copy functions to circumvent pygame not allowing for deepcopy of
        pygame surfaces
        """
        super(Entity, self).__init__()
        ######################
        #game attributes
        ######################
        self.jumping = False
        self.running = False
        self.onGround = False
        self.crouching = False
        self.move_frame = 0
        ######################
        # entity attributes
        ######################
        if copy_vals is None:
            attr_fl = open(curr_path+"attributes.txt", "r")
            attr_list = list(map(lambda x: [x[0],ut.t_convert(x[1])], [i.split("=") for i in attr_fl.read().replace(' ', "")\
                            .split("\n") if i.strip() != ""]))
            if verbose: print(content_list)
            
            attr_fl.close()
            for a,v in attr_list:
                setattr(self,a,v)
            ######################
            #animations
            ######################
            # {        run:{left:[], right:[]}    }
            self.state_dict = {}
            self.state_frames = {}
            self.state_inc = {}
            #run right or left same frames
            # run: 10 e.t.c.
            
            self.name = name
            self.image = pg.image.load(curr_path+"base.png")
            self.image = self.resize_img(self.image)
            self.rect = self.image.get_rect()
            self.load_sprites(curr_path)
        else:
            self.state_dict = copy_vals["state_dict"]
            self.state_frames = copy_vals["state_frames"]
            self.state_inc = copy_vals["state_inc"]
            self.name = copy_vals["name"]
            self.image = copy_vals["image"]
            self.rect = self.image.get_rect()
        # print(self.rect.size)
        
        
    def load_sprites(self,curr_path):            
        #load sprites
        dirs, poo = ut.get_dirs(curr_path+"sprites",prepended=True)
        # print(dirs)
        if hasattr(self, "moving_entity"):
            for spr in dirs:
                fls, pth =  ut.get_files(curr_path+"sprites"+"\\"+spr,".png" ,prepended=True)
                
                self.state_frames[spr]=len(fls)
                self.state_inc[spr]=float(60/len(fls))/20
                #if self.moving_entity
                self.state_dict[spr]={
                    1: [],#right=1
                    -1 : [],#left=-1
                    'base' : []
                    }
                resizing = curr_path+"sprites"+"\\"+spr+"\\sizing.txt"
                # print(resizing)
                resizeX = None
                if os.path.exists(resizing):
                    fl_tmp = open(resizing)
                    resizeX = ut.t_convert(fl_tmp.read())
                    fl_tmp.close()
                    
                for f in fls:
                    #default sprites are oriented to the left
                    img_left = pg.image.load(pth+f)

                    
                    img_left=self.resize_img(img_left,sprite_ratio = resizeX)
                    #build right image
                    img_right = pg.transform.flip(img_left, True, False)
                    self.state_dict[spr][1].append(img_right)#right
                    self.state_dict[spr][-1].append(img_left)#left
        else:
            for spr in dirs:
                fls, pth =  ut.get_files(curr_path+"sprites"+"\\"+spr,".png" ,prepended=True)
                
                self.state_frames[spr]=len(fls)
                self.state_dict[spr]={
                    'idle' : []
                    }
                for f in fls:
                    #default sprites are oriented to the left
                    img_base = pg.image.load(pth+f)
                    img_base=self.resize_img(img_left)
                    #build right image
                    img_base = pg.transform.flip(img_left, True, False)
                    self.state_dict[spr]['idle'].append(img_base)

            
    def resize_img(self,image,cX = None, cY =None,sprite_ratio=None):
        
        newX, newY = 0,0
        oldx, oldy = image.get_rect().size
        if sprite_ratio is not None:
            ratio = (screen_width/oldx)/sprite_ratio
            return pg.transform.scale(image, (int(oldx*ratio), int(oldy*ratio)))            
        if cX is None and cY is None:
            #resize to sprite-to screen ratio in attributes.txt
            ratio = (screen_width/oldx)/self.sprite_screen_ratio
            return pg.transform.scale(image, (int(oldx*ratio), int(oldy*ratio)))
        elif cX is not None and cY is None:
            ratio = (cX/oldx)/self.sprite_screen_ratio
            return pg.transform.scale(image, (int(oldx*ratio), int(oldy*ratio)))
        elif cY is not None and cX is None:
            ratio = (cY/oldy)/self.sprite_screen_ratio
            return pg.transform.scale(image, (int(oldx*ratio), int(oldy*ratio)))
        else:
            ratioX = (cX/oldx)/self.sprite_screen_ratio
            ratioY = (cY/oldy)/self.sprite_screen_ratio
            return pg.transform.scale(image, (int(oldx*ratioX), int(oldy*ratioY)))
        return image     
        
    

    
    def update(self):
        #placeholder
        pass


class moving_entity(Entity):
    
    def __init__(self, name,curr_path,scale = None,verbose = False,copy_vals = None):
        
        #positino & direction
        self.vx = 0
        self.pos = vec((0, 0))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = 1#"right"
        self.state = "idle"
        
        ###
        self.accel=0
        self.velocity=0
        self.attack=0
        self.range=0
        self.damage=0
        self.cooldown = 0 #
        
        if  copy_vals is None:
            super(moving_entity, self).__init__(name,curr_path,scale = None,verbose = False)
            print(self.max_hp)
            # print("asdfasdfadfsaf")
            self.hp = self.max_hp
        else:
            super(moving_entity, self).__init__(None,None,copy_vals=copy_vals)
            self.hp=0
            self.max_hp = 0

    def copy(self):
        copy_vals = {
            "state_dict":self.state_dict,
            "state_frames":self.state_frames,
            "state_inc":self.state_inc,
            "name":self.name,
            "image":self.image
        }
        ret = moving_entity(None,None,copy_vals=copy_vals)
        
        ret.accel=self.accel
        ret.velocity=self.velocity
        ret.attack=self.attack
        ret.range=self.range
        ret.max_hp = self.max_hp
        ret.cooldown = self.cooldown
        ret.damage = self.damage
        ret.hp = ret.max_hp

        return ret
        

    def reset(self):

        self.hp=self.max_hp
        
    def set_pos(self,posX,posY):
        self.pos = vec(posX,posY)
    
    def do_attack(self,attack_in = None):
        attack_in = attack_in if attack_in is not None else self.attack
    
        if self.cooldown <=0:
            attack_ent = game_attacks[attack_in].copy()
            self.cooldown+=(attack_ent.cooldown*FPS)
            tmp_a = Attack(self,self.pos,game_attacks[attack_in].copy(),self.direction) 
            return [tmp_a]
        else:
            return []
    
    def jump(self):
        # self.hp=0
        # If touching the ground, and not currently jumping, cause the player to jump.
        if self.onGround and not self.jumping:
            self.state="jumping"
            self.onGround = False
            self.jumping = True
            self.vel.y = -50
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc  #
            self.rect.midbottom = self.pos

    def move(self):
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  #
        self.rect.midbottom = self.pos
        
    def move_no_friction(self):
        self.acc.x += self.vel.x 
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  #
        self.rect.midbottom = self.pos
        
    def stop(self):
       self.vel.x=0
       self.acc.x=0
    

    def draw_hp_bar(self,screen):
        #perhaps add name or other attributes
        pg.draw.rect(screen, (255,0,0), (self.rect.topleft[0], self.rect.topleft[1] , self.rect.size[0], 10)) 
        pg.draw.rect(screen, (0,128,0), (self.rect.topleft[0], self.rect.topleft[1] , self.rect.size[0]*(self.hp/self.max_hp), 10))
        
    def update(self,screen):
        """
        update moving entity
        """
        #draw hp bar
        self.draw_hp_bar(screen)
        self.move()
        self.update_sprite(screen)
        
        
        

    def update_sprite(self,screen):
        if self.hp>0:
            if self.onGround:
                if abs(self.vel.x) > 0.3:
                    
                    self.running = True
                    self.state = "run"
                else:
                    self.running = False
                    self.state = "idle"
                
            # if self.jumping == False and self.running == True:  
            if self.vel.x > 0:
                self.direction = 1#right=1
            elif self.vel.x < 0:
                self.direction = -1#left=-1
                
            if self.state != "idle" and abs(self.vel.x) < 0.2 and self.move_frame != 0:
                self.move_frame = 0
        else:
            self.state="dead"



        self.move_frame += self.state_inc[self.state]
        
        if  self.move_frame> self.state_frames[self.state]-1:
            self.move_frame=0
        # print(self.state_frames[self.state])
        self.image = self.state_dict[self.state][self.direction][ int(self.move_frame)]
        # else:
            # self.state = "dead"
        screen.blit(self.image, self.rect)
        
class Player(object):
    def __init__(self,entity, level = None):
        self.attacks = []
        #make list of entities
        global game_entities
        if entity in game_entities.keys():
            self.entity = game_entities[entity].copy()
            
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
                if blue:
                    self.attacks+=self.entity.do_attack("fireball")         
                if red:
                    self.attacks+=self.entity.do_attack()   
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
                a.update(screen)
        
        # if pressed_keys[pg.K_r]:
        #     self.entity.reset()
                

class Attack(object):
    """
    attack class, 
    attacks have pngs, range, damage and attributes,
    die after exceed range
    """
    def __init__(self,sender, pos, entity, direction,level = None):
        global game_attacks
        self.dead = False
        self.entity = entity
        self.entity.pos = vec(pos.x,pos.y)
        self.entity.vel = vec(self.entity.velocity*direction,0)
        self.entity.acc = vec(self.entity.accel*direction,0)
        if entity in game_entities.keys():
            self.entity = game_attacks[entity].copy()
        
    
    def update(self,screen):
        
        if self.entity.pos.x>screen_width or self.entity.pos.y >screen_height\
            or self.entity.pos.x<0 or  self.entity.pos.y<0:
                self.hp=0
                self.entity.pos.x=0
                self.entity.acc.x = 0
                self.dead= True
        else:
            self.entity.move_no_friction()
            self.entity.update_sprite(screen)
            self.entity.hp-=1
        
        
class Enemies(moving_entity):
    def __init__(self,entity,posX=0,posY=0):    
        #make list of entities
        self.entity = game_enemies[entity].copy()
        self.entity.set_pos(posX,posY)
    def update(self,screen):
        
        self.entity.stop()
        self.entity.update(screen)
        #depending on attack strategy, employ different one
        ###ADD AI
        
        pass

class Enemy(pg.sprite.Sprite):

    def __init__(self, pos):
        super(Enemy, self).__init__()
        self.image = pg.Surface((120, 120), pg.SRCALPHA)
        pg.draw.circle(self.image, (240, 100, 0), (60, 60), 60)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pg.mask.from_surface(self.image)
    
    



#################################
# Level, bg & terrain
#################################
class Level(object):
    def __init__(self, name, curr_path):
        self.x = 1;
        self.curr_path = curr_path
        self.bg =Background(curr_path)
        self.terrain =Background(curr_path,name = "terrain.png")
        self.collidebg=pg.sprite.Group(self.terrain)
        self.mov_entities = []
        self.alive_enemies = []
        self.enemies = []
        self.attacks = []
        self.load_entities()
        self.screen = None
        
        
    def load_entities(self, reset = False):
        global glob_player
        #load entities, set each to alive
        attr_fl = open(self.curr_path+"placement.txt", "r")
        attr_list = list(map(lambda x: [x[0],           list(map(lambda y: ut.t_convert(y),x[1].strip().split(",")) )],\
                    [i.split("=") for i in attr_fl.read().replace(' ', "")\
                        .split("\n") if i.strip() != ""]))
        attr_fl.close()
        print(glob_player)
        if not reset:
            for k,v in attr_list:
                if k == "player":
                    glob_player.entity.set_pos(v[0],v[1])
                    self.mov_entities.append(glob_player)
                else:
                    tmp = Enemies(k,posX=v[0],posY=v[1])
                    self.enemies.append(tmp)
                    self.alive_enemies.append(tmp)
                    self.mov_entities.append(tmp)
        else:
            for m,v in zip(self.mov_entities,list(map(lambda x: x[1],attr_list))):
                # print(v)
                m.entity.set_pos(v[0],v[1])
                m.entity.reset()
            

        
    
    def reset(self):
        #reset entities and their positions
        # Loading screen?
        self.attacks = []
        self.load_entities(reset=True)
        

    def update(self):
        self.bg.update(self.screen)
        self.terrain.update(self.screen)
        #player
        ###########################
        # Collision Checking
        ###########################
        #--------------------------
        #apply gravity and terrain check
        #--------------------------
        for m in self.mov_entities:
            m.entity.acc.y=+3;
            # m.acc.y=+3;
            self.terrain_check(m.entity)
            m.update(self.screen)
        #--------------------------
        #attack collision: Player attacks to enemies
        #--------------------------
        for a in glob_player.attacks:
            for m in self.alive_enemies:
                if a.entity.rect.colliderect(m.entity.rect):
                    m.entity.hp-=a.entity.damage
                    a.dead = True
            # .colliderect(m.entity.rect)
        
        #--------------------------
        # entity - entity collision
        #--------------------------
        # self.alive_enemies
        
        
        
    def terrain_check(self,moving_ent):
        """
        naive collision handling with background sprite
        """
        #apply gravity if no collision
        hits = pg.sprite.spritecollide(moving_ent, pg.sprite.Group(self.terrain), False, pg.sprite.collide_mask)
        if hits:
            moving_ent.vel.y = 0
            moving_ent.acc.y = 0
            moving_ent.jumping = False
            moving_ent.onGround = True
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

    def collision_entities(self):
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
        self.image = resize_img(self.image,cY=screen_height)
        self.rect = self.image.get_rect(center=(int(screen_width/2),int(screen_height/2)))
        self.mask = pg.mask.from_surface(self.image)
        # print(self.rect.size)

 
    def update(self,screen):
        screen.blit(self.image, (self.pos.x, self.pos.y))
        
        
def resize_img(image,cX = None, cY =None):

    oldx, oldy = image.get_rect().size
    if cX is None and cY is None:
        return image
    elif cX is not None and cY is None:
        ratio = (cX/oldx)
        return pg.transform.scale(image, (int(oldx*ratio), int(oldy*ratio)))
    elif cY is not None and cX is None:
        ratio = (cY/oldy)
        return pg.transform.scale(image, (int(oldx*ratio), int(oldy*ratio)))
    else:
        ratioX = (cX/oldx)
        ratioY = (cY/oldy)
        return pg.transform.scale(image, (int(oldx*ratioX), int(oldy*ratioY)))
    return image     
#####################################     






class Game:
    def __init__(self):
        global glob_player, game_levels
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.player =  glob_player
        self.game_state=1
        self.level = "level_1"
        
        for k,v in game_levels.items():
            v.player= self.player
            v.screen = self.screen
            # v.mov_entities.append(self.player.entity)
            print()
        # self.enemies = pg.sprite.Group(Enemy((320, 240)))
        # self.all_sprites = pg.sprite.Group(self.player.entity, self.enemies)
        self.done = False
        self.clock = pg.time.Clock()

    def run(self):
        while not self.done:
            self.event_loop()
            
            game_levels[self.level].update()
            # self.update()

            pg.display.flip()
            #set fps pi 30 fps bc Raspberry pi is a potato
            self.clock.tick(FPS)
            
            
            
            #self.clock.tick(60)
    def reset_level(self,level = None):
        # self.resetting = True
        level = self.level if level is None else level
        game_levels[level].reset()
        # self.resetting = False
        
    def event_loop(self):
        if USE_ESP:
            get_serial()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
        pressed_keys = pg.key.get_pressed()
        
        
        if pressed_keys[pg.K_r]:
            self.reset_level()
            


    def main_menu(self):
        pass

def load_entities(verbose = False):
    global game_entities, game_enemies, game_attacks
    char_dir = "\\bin\\characters"

    #characters
    dirs, curr_path = ut.get_dirs("\\bin\\characters")
    for i in dirs:
        if verbose :
            print(i)
        ok = curr_path+i+"\\"
        print(ok)
        # print(os.listdir(ok))
        game_entities[i] = moving_entity(i,curr_path+i+"\\")
        #if you want to fight your own characters
        game_enemies[i] = moving_entity(i,curr_path+i+"\\")
    #enemies
    dirs, curr_path = ut.get_dirs("\\bin\\enemies")
    for i in dirs:
        if verbose :
            print(i)
        ok = curr_path+i+"\\"
        print(ok)
        # print(os.listdir(ok))
        game_enemies[i] = moving_entity(i,curr_path+i+"\\")
    dirs, curr_path = ut.get_dirs("\\bin\\attacks")
    for i in dirs:
        if verbose :
            print(i)
        ok = curr_path+i+"\\"
        print(ok)
        # print(os.listdir(ok))
        game_attacks[i] = moving_entity(i,curr_path+i+"\\")
    #levels
    
    
def load_levels(verbose = False):
    global game_levels
    char_dir = "\\bin\\levels"

    #characters
    dirs, curr_path = ut.get_dirs("\\bin\\levels")
    for i in dirs:
        if verbose :
            print(i)
        ok = curr_path+i+"\\"
        print(ok)
        # print(os.listdir(ok))
        game_levels[i] = Level(i,curr_path+i+"\\")
    pass
################################################################
#serial
################################################################

    
def get_serial():
    global CONTROL_VAL
    data = ser.read(1)
    data+= ser.read(ser.inWaiting())
    if len(data) == 5:
        CONTROL_VAL = int(data[:3])


            
def run_game():

    #load levels
    pg.init()
    game = Game()
    game.run()
    pg.quit()
if __name__ == '__main__':

    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    load_entities()
    glob_player=Player('jeanne')
    load_levels()
    get_serial()
    run_game()

    
    # print(os.listdir(os.getcwd()+"\\bin\\characters"))