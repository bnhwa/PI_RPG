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
import copy
##globals
game_entities = {}
game_levels = {}

#screenx screeny
root = Tk() 
screen_height = root.winfo_screenheight() 
screen_width = root.winfo_screenwidth()
#screen_height,screen_width = int(screen_height/2),int(screen_width/2)
print(screen_width,screen_height)
#https://gamedev.stackexchange.com/questions/105532/pygame-implementing-a-scrolling-camera
#https://stackoverflow.com/questions/20180594/pygame-collision-by-sides-of-sprite
##
vec = pg.math.Vector2
ACC = 5#0.7
FRIC = -0.10
FPS = 60
FPS_CLOCK = pg.time.Clock()
COUNT = 0
#################################
# Entities
#################################

class Entity(pg.sprite.Sprite):
    
    def __init__(self, name, curr_path,scale = None,verbose = False):
        super(Entity, self).__init__()
        ######################
        # entity attributes
        ######################
        
        attr_fl = open(curr_path+"attributes.txt", "r")
        attr_list = list(map(lambda x: [x[0],ut.t_convert(x[1])], [i.split("=") for i in attr_fl.read().replace(' ', "")\
                        .split("\n") if i.strip() != ""]))
        if verbose: print(content_list)
        
        attr_fl.close()
        for a,v in attr_list:
            setattr(self,a,v)
            
        ######################
        #game attributes
        ######################
        self.jumping = False
        self.running = False
        self.crouching = False
        self.move_frame = 0
        ######################
        #animations
        ######################
        self.state_dict = {}
        # {        run:{left:[], right:[]}    }
        self.state_frames = {}
        #run right or left same frames
        # run: 10 e.t.c.
        
        self.name = name
        self.image = pg.image.load(curr_path+"base.png")
        self.image = self.resize_img(self.image)
        self.rect = self.image.get_rect()
        print(self.rect.size)
        # if scale is not None:
            
        #     oldx, oldy = self.image.get_rect().size
        #     self.image = pg.transform.scale(picture, (oldx*2, oldy*2))
        
        #open attributes.txt
        
        
        if verbose:
            print(self.rect.size)
            print(curr_path)
            
        #load sprites
        dirs, poo = ut.get_dirs(curr_path+"sprites",prepended=True)
        # print(dirs)
        if self.moving_entity:
            for spr in dirs:
                fls, pth =  ut.get_files(curr_path+"sprites"+"\\"+spr,".png" ,prepended=True)
                
                self.state_frames[spr]=len(fls)
                #if self.moving_entity
                self.state_dict[spr]={
                    'right': [],
                    'left' : [],
                    'base' : []
                    }
                for f in fls:
                    #default sprites are oriented to the left
                    img_left = pg.image.load(pth+f)
                    img_left=self.resize_img(img_left)
                    #build right image
                    img_right = pg.transform.flip(img_left, True, False)
                    self.state_dict[spr]['right'].append(img_right)
                    self.state_dict[spr]['left'].append(img_left)
        else:
            for spr in dirs:
                fls, pth =  ut.get_files(curr_path+"sprites"+"\\"+spr,".png" ,prepended=True)
                
                self.state_frames[spr]=len(fls)
                self.state_dict[spr]={
                    'base' : []
                    }
                for f in fls:
                    #default sprites are oriented to the left
                    img_base = pg.image.load(pth+f)
                    img_base=self.resize_img(img_left)
                    #build right image
                    img_base = pg.transform.flip(img_left, True, False)
                    self.state_dict[spr]['base'].append(img_base)

            
    def resize_img(self,image,cX = None, cY =None):
        
        newX, newY = 0,0
        oldx, oldy = image.get_rect().size
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
        
    
    
    def imgs_state_dict(self):
        pass

    
    def update(self):
        
        pass


class moving_entity(Entity):
    
    def __init__(self, name,curr_path,scale = None,verbose = False):
        super(moving_entity, self).__init__(name,curr_path,scale = None,verbose = False)
        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "right"
        self.state = "idle"
        
    def move(self):
        
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  #
        # self.rect.midbottom = self.pos
        self.rect.center = self.pos
        
        pass
    def attack(self):
        pass
    
    def jump(self,terrain):
        self.rect.x += 1
     
        # Check to see if payer is in contact with the ground
        hits = pg.sprite.spritecollide(self, terrain, False)
         
        self.rect.x -= 1
     
        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -12
       
       
    def stop(self):
        self.vel.x=0
        self.acc.x=0
        
    def update(self,screen):
        #self.state
        #self.image = 
        # self.move()
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  #
        self.rect.midbottom = self.pos
        #self.rect.center = self.pos
        # print(self.pos)
        if abs(self.vel.x) > 0.3:
            self.running = True
            self.state = "run"
        else:
            self.running = False
            self.state = "idle"
        if self.jumping == False and self.running == True:  
              if self.vel.x > 0:
                    self.direction = "right"
              elif self.vel.x < 0:
                    self.direction = "left"
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0

        self.move_frame += 0.5
        
        if  self.move_frame> self.state_frames[self.state]-1:
            self.move_frame=0
        # print(self.state_frames[self.state])
        self.image = self.state_dict[self.state][self.direction][ int(self.move_frame)]
        screen.blit(self.image, self.rect)


class Player1(object):
    def __init__(self,entity):
        
        #make list of entities
        global game_entities
        if entity in game_entities.keys():
            self.entity = copy.copy(game_entities[entity])
            
        # super(Player1, self).__init__(name,curr_path)
    def update(self,screen):
        
        # print(self.entity.pos)
        
        self.entity.update(screen)
        pressed_keys = pg.key.get_pressed()
        self.state = "idle"
        self.entity.stop()
        if pressed_keys[pg.K_LEFT]:
            # self.entity.move()
            # self.state = "run"
            # print(self.entity.pos)
            self.entity.acc.x = -self.entity.accel
        if pressed_keys[pg.K_RIGHT]:
            # self.entity.move()
            # self.state = "run"
            self.entity.acc.x = self.entity.accel#ACC 
        # if pressed_keys[pg.K_DOWN]:
        #     self.state="crouch"

class attack(Entity):
    
    """
    attack class, 
    attacks have pngs, range, damage and attributes,
    die after exceed range
    """
    
    def __init__(self, name,curr_path,scale = None):
        super(Player1, self).__init__(name,curr_path)
        #attributes.txt
        
        
        
class Player(pg.sprite.Sprite):

    def __init__(self, pos):
        super(Player, self).__init__()
        

        
        self.image = pg.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect()
        
        self.image = pg.Surface((120, 120), pg.SRCALPHA)
        pg.draw.polygon(self.image, (0, 100, 240), [(60, 0), (120, 120), (0, 120)])
        self.rect = self.image.get_rect(center=pos)
        self.mask = pg.mask.from_surface(self.image)
    def loadImages(self):
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
        self.bg =Background(curr_path)
        self.terrain =Background(curr_path,name = "terrain.png")
        self.collidebg=pg.sprite.Group(self.terrain)
        self.mov_entities = []
        
        
    def load_entities(self):
        pass
    
        
    def update(self,screen):
        self.bg.update(screen)
        self.terrain.update(screen)
        ###########################
        # Collision Checking
        ###########################
        #apply gravity and terrain check with 
        for m in self.mov_entities:
            m.acc.y=+3;
            self.terrain_check(m)
        
        
    def terrain_check(self,moving_ent):
        #apply gravity if no collision
        hits = pg.sprite.spritecollide(moving_ent, pg.sprite.Group(self.terrain), False, pg.sprite.collide_mask)
        # if moving_ent.vel.y > 0:
        if hits:
            # print("faw")
            lowest = hits[0]
            moving_ent.vel.y = 0
            moving_ent.acc.y = 0
            moving_ent.jumping = False
            #only for individual rectangles
            # if moving_ent.pos.y < lowest.rect.bottom:
            #     # moving_ent.pos.y = lowest.rect.top + 1
            #     moving_ent.vel.y = 0
            #     moving_ent.acc.y = 0
            #     moving_ent.jumping = False
        # else:
        # #apply gravity if no collision
        #     pg.display.set_caption('falling')
            # moving_ent.acc.y=+9;

    def rect_check(self,moving_ent):
        #collision handling with individual platforms
        #apply gravity if no collision
        hits = pg.sprite.spritecollide(moving_ent, pg.sprite.Group(self.terrain), False, pg.sprite.collide_mask)
        # if moving_ent.vel.y > 0:
        if hits:
            #only for individual rectangles
            if moving_ent.pos.y < lowest.rect.bottom:
                # moving_ent.pos.y = lowest.rect.top + 1
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
        # self.bgY = 0
        # self.bgX = 0
        self.pos  = vec(0,0)
        if name is None:
            self.image = pg.image.load(curr_path+"background.png")
        else:
            self.image = pg.image.load(curr_path+name)
        self.image = resize_img(self.image,cX=screen_width)
        self.rect = self.image.get_rect(center=(int(screen_width/2),int(screen_height/2)))
        self.mask = pg.mask.from_surface(self.image)
        print(self.rect.size)

 
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
        self.screen = pg.display.set_mode((screen_width, screen_height))
        # self.player = Player((20, 20))
        self.player =  Player1('jeanne')
        
        self.level = "level_1"
        
        for k,v in game_levels.items():
            v.mov_entities.append(self.player.entity)
            print()
        self.enemies = pg.sprite.Group(Enemy((320, 240)))
        # self.all_sprites = pg.sprite.Group(self.player.entity, self.enemies)
        self.done = False
        self.clock = pg.time.Clock()

    def run(self):
        while not self.done:
            self.event_loop()
            game_levels[self.level].update(self.screen)
            self.update()

            self.player.update(self.screen)
            pg.display.flip()
            self.clock.tick(60)
            #self.clock.tick(60)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            # elif event.type == pg.MOUSEMOTION:
            #     self.player.entity.rect.center = event.pos

    def update(self):


        
        
        
        
        
        if pg.sprite.spritecollide(self.player.entity, self.enemies, False, pg.sprite.collide_mask):
            pg.display.set_caption('collision')
        else:
            pg.display.set_caption('no collision')

    # def draw(self):
    #     pass
    #     # self.screen.fill((30, 30, 30))
    #     self.all_sprites.draw(self.screen)

def load_entities(verbose = False):
    global game_entities
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


if __name__ == '__main__':
    #load entities
    load_entities()
    load_levels()
    #load levels
    pg.init()
    game = Game()
    game.run()
    pg.quit()
    # print(os.listdir(os.getcwd()+"\\bin\\characters"))