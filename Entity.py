# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 12:29:57 2021

@author: bb339
"""

from global_vars import *
import os
import pygame as pg
import game_utils as ut


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
        
    def rep_sprite(self,orig,new):

        self.state_dict[new]={
                    1: [],#right=1
                    -1 : [],#left=-1
                    }
        self.state_dict[new][1]=self.state_dict[orig][1]
        self.state_dict[new][-1]=self.state_dict[orig][-1]
        self.state_frames[new]=self.state_frames[orig]
        self.state_inc[new]=self.state_inc[orig]
        # print(len(self.state_dict[new][1]))
        # print(len(self.state_dict[orig][1]))
        
    def load_sprites(self,curr_path):            
        #load sprites
        dirs, poo = ut.get_dirs(curr_path+"sprites",prepended=True)
        # print(dirs)
        if hasattr(self, "moving_entity"):
            # print(dirs)
            for spr in dirs:
                fls, pth =  ut.get_files(curr_path+"sprites"+"/"+spr,".png" ,prepended=True)
                
                self.state_frames[spr]=len(fls)
                self.state_inc[spr]=float(60/len(fls))/20
                #if self.moving_entity
                self.state_dict[spr]={
                    1: [],#right=1
                    -1 : [],#left=-1
                    }
                resizing = curr_path+"sprites"+"/"+spr+"/sizing.txt"
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
            if 'dying' not in dirs:
                self.rep_sprite('dead','dying')
            if 'crouch' not in dirs:
                self.rep_sprite('idle','crouch')
            # for i in ['jumping','run']:
            #     if i not in dirs:
            #         self.rep_sprite('idle',i)

        else:
            for spr in dirs:
                fls, pth =  ut.get_files(curr_path+"sprites"+"/"+spr,".png" ,prepended=True)
                
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
        ###
        self.dead = False
        
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
        global OFFSET
        copy_vals = {
            "state_dict":self.state_dict,
            "state_frames":self.state_frames,
            "state_inc":self.state_inc,
            "name":self.name,
            "image":self.image
        }
        ret = moving_entity(None,None,copy_vals=copy_vals)
        
        ret.accel=self.accel*OFFSET
        ret.velocity=self.velocity*OFFSET
        ret.attack=self.attack
        ret.range=self.range*OFFSET
        ret.max_hp = self.max_hp
        ret.cooldown = self.cooldown
        ret.damage = self.damage
        ret.hp = ret.max_hp

        return ret
        

    def reset(self):
        self.dead == False
        self.jumping = False
        self.running = False
        self.onGround = False
        self.crouching = False
        self.state = "idle"
        self.move_frame=0
        self.hp=self.max_hp
        print("{} reset".format(self.name))
        # print(self.state)
        
    def set_pos(self,posX,posY):
        self.pos = vec(posX,posY)
    
    def do_attack(self,game, attack_id,attack_in = None):
        attack_in = attack_in if attack_in is not None else self.attack
    
        if self.cooldown <=0:
            attack_ent = game.game_attacks[attack_in].copy()
            self.cooldown+=(attack_ent.cooldown*FPS)
            tmp_a = Attack(self,self.pos,attack_ent,self.direction,attack_id) 
            return [tmp_a]
        else:
            return []
    def crouch(self):
        if self.onGround and not self.crouching:
            self.crouching = True
            self.state = "crouch"
            
    def jump(self):
        # self.hp=0
        # If touching the ground, and not currently jumping, cause the player to jump.
        if self.onGround and not self.jumping :#and not self.crouching:
            self.state="jumping"
            self.onGround = False
            self.jumping = True
            self.vel.y = -50*OFFSET
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
        if self.hp >0:
            pg.draw.rect(screen, (255,0,0), (self.rect.topleft[0], self.rect.topleft[1] , self.rect.size[0], 10)) 
            pg.draw.rect(screen, (0,128,0), (self.rect.topleft[0], self.rect.topleft[1] , self.rect.size[0]*(self.hp/self.max_hp), 10))
        
    def update(self,screen):
        """
        update moving entity
        """
        #draw hp bar
        self.draw_hp_bar(screen)
        self.move()
        self.update_sprite()
    
        
        

    def update_sprite(self):
        if self.hp>0:
            #self.hp>0:
            if self.onGround:
                if not self.crouching:
                    if abs(self.vel.x) > 0.3:
                        
                        self.running = True
                        self.state = "run"
                    else:
                        self.running = False
                        self.state = "idle"
                else:
                    self.crouching = False
                
            # if self.jumping == False and self.running == True:  
            if self.vel.x > 0:
                self.direction = 1#right=1
            elif self.vel.x < 0:
                self.direction = -1#left=-1
                
            if (self.state not in  ["idle","crouch"] )and abs(self.vel.x) < 0.2 and self.move_frame != 0:
                self.move_frame = 0
            self.crouching ==False
        elif not self.state == "dead":#not self.dead: #self.state != "dead":
            self.state = "dying"
        else:
            self.state = "dead"


            

        # else:
            # self.state = "dead"
    def render(self, screen):
        self.move_frame += self.state_inc[self.state]
        
        if  self.move_frame> self.state_frames[self.state]-1:
            self.move_frame=0
        self.image = self.state_dict[self.state][self.direction][ int(self.move_frame)]
        screen.blit(self.image, self.rect)
class Attack(object):
    """
    attack class, 
    attacks have pngs, range, damage and attributes,
    die after exceed range
    """
    def __init__(self,sender, pos, entity, direction,attack_id):
        # print(attack_id)
        self.attack_id = attack_id
        self.dead = False
        self.entity = entity
        self.entity.pos = vec(pos.x,pos.y)
        self.entity.vel = vec(self.entity.velocity*direction,0)
        self.entity.acc = vec(self.entity.accel*direction,0)
        self.entity = entity
        
    
    def update(self,screen):
        
        if self.entity.pos.x>screen_width or self.entity.pos.y >screen_height\
            or self.entity.pos.x<0 or  self.entity.pos.y<0:
                self.hp=0
                self.entity.pos.x=0
                self.entity.acc.x = 0
                self.dead= True
        else:
            self.entity.move_no_friction()
            self.entity.update_sprite()
            self.entity.render(screen)
            self.entity.hp-=1
            
