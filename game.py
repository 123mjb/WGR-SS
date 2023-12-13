import pygame
from pygame.locals import *
import pygame.gfxdraw
import random
import math
import json

with open("levels.json","r") as read:
    lvlsobj = json.load(read)
    print(lvlsobj)
pygame.init()
FPS = 60
clock = pygame.time.Clock()
screensize = (1280,720)
screen = pygame.display.set_mode(screensize)
running = True
white = (255,255,255)
class Sprite(pygame.sprite.Sprite):
    def __init__(self, colour,height,width) -> None:
        super().__init__()
        self.sprint = False
        self.wj = False
        self.oheight = height
        self.owidth = width
        self.adheight = height
        self.adwidth = width
        self.adjustmenth = 1
        self.adjustmentw = 1
        self.progression = 0
        self.colour = colour
        self.rs = [i/12 for i in range(1,12)]
        self.degs = [random.randrange(0,360) for _ in range(0,len(self.rs))]
        self.jumping = False
        self.crouching = False
        self.ymoment = 0
        self.sincestartofjump = 0
        self.falling = False
        
        head_width = width/5
        head_height = height/4
        shoulder_height = height/8
        arm_width = width/5
        body_width = width/2
        legs_height = height*5/16
        body_height = height-(head_height+shoulder_height+legs_height)

        self.image = pygame.Surface([width,height])
        #head
        pygame.draw.rect(self.image,colour,pygame.Rect((width-head_width)/2,0,head_width,head_height))
        #shoulders
        pygame.draw.rect(self.image,colour,pygame.Rect(0,head_height,width,shoulder_height))
        # arms
        pygame.draw.rect(self.image,colour,pygame.Rect(0,head_height+shoulder_height,arm_width,body_height))
        pygame.draw.rect(self.image,colour,pygame.Rect(width-arm_width,head_height+shoulder_height,arm_width,body_height))
        # body
        pygame.draw.rect(self.image,colour,pygame.Rect((width-body_width)/2,head_height+shoulder_height,body_width,body_height))
        #legs
        pygame.draw.rect(self.image,colour,pygame.Rect((width-body_width)/2,head_height+shoulder_height+body_height,body_width*7/16,legs_height))
        pygame.draw.rect(self.image,colour,pygame.Rect((width-body_width)/2+body_width*9/16,head_height+shoulder_height+body_height,body_width*7/16+1,legs_height))
        
        self.rect = self.image.get_rect()
    def movesideways(self,direction):
        self.adwidth = self.owidth * self.adjustmentw
        self.adheight = self.owidth * self.adjustmenth
        self.image = pygame.Surface([self.adwidth,self.adheight])
        draw_rect_alpha(self.image,self.image.get_rect())
        self.progression +=10*direction*-1
        if self.progression > 359: self.progression = 0
        adjusted_colour = (255-self.colour[0],255-self.colour[1],255-self.colour[2])
        pygame.gfxdraw.filled_circle(self.image,int(round(self.adwidth/2)),int(round(self.adheight/2)),int(round(self.adwidth/2)),self.colour)
        pygame.gfxdraw.circle(self.image,int(round(self.adheight/2)),int(round(self.adheight/2)),int(round(self.adwidth/2)),self.colour)
        try: s
        except NameError: s=0
        if self.progression % 20 == 0: s = random.randrange(0,5)
        for i in range(0,len(self.rs)):
            pygame.draw.arc(self.image,adjusted_colour,Rect(int(round((self.adheight-self.adheight*self.rs[i])/2)),int(round((self.adheight-self.adheight*self.rs[i])/2)),int(round(self.adheight*self.rs[i])),int(round(self.adheight*self.rs[i]))),math.radians(self.progression+self.degs[i]),math.radians(self.progression+self.degs[i]+45+s),int(round(self.adwidth/2/15)))      
    def jump(self):
        self.adheight = self.oheight * self.adjustmenth
        self.adwidth = self.owidth * self.adjustmentw
        self.image = pygame.Surface([self.adwidth,self.adheight])

        head_width = self.adwidth/5
        head_height = self.adheight/4
        shoulder_height = self.adheight/8
        arm_width = self.adwidth/5
        body_width = self.adwidth/2
        legs_height = self.adheight*5/16
        body_height = self.adheight-(head_height+shoulder_height+legs_height)
        draw_rect_alpha(self.image,self.image.get_rect())
        #head
        pygame.draw.rect(self.image,self.colour,pygame.Rect((self.adwidth-head_width)/2,0,head_width,head_height))
        #shoulders
        pygame.draw.rect(self.image,self.colour,pygame.Rect(0,head_height,self.adwidth,shoulder_height))
        # arms
        pygame.draw.rect(self.image,self.colour,pygame.Rect(0,head_height+shoulder_height,arm_width,body_height))
        pygame.draw.rect(self.image,self.colour,pygame.Rect(self.adwidth-arm_width,head_height+shoulder_height,arm_width,body_height))
        # body
        pygame.draw.rect(self.image,self.colour,pygame.Rect((self.adwidth-body_width)/2,head_height+shoulder_height,body_width,body_height))
        #legs
        pygame.draw.rect(self.image,self.colour,pygame.Rect((self.adwidth-body_width)/2,head_height+shoulder_height+body_height,body_width*7/16,legs_height))
        pygame.draw.rect(self.image,self.colour,pygame.Rect((self.adwidth-body_width)/2+body_width*9/16,head_height+shoulder_height+body_height,body_width*7/16+1,legs_height))
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LSHIFT]:
            self.sprint = True
        else: self.sprint = False
        if pressed_keys[K_w] or pressed_keys[K_SPACE]:
            self.jump()
            self.jumping = True
            if not self.falling or self.wj:
                self.ymoment = 17
        else: self.jumping = False
        if pressed_keys[K_s]:
            self.crouching = True
        if pressed_keys[K_a]:
            if self.rect.left > 0:
                self.movecheck(-7 if self.sprint else -5)
                if not self.falling: self.movesideways(-1)
        if pressed_keys[K_d]:
            if self.rect.right < screen.get_width():
                self.movecheck(7 if self.sprint else 5)
                if not self.falling: self.movesideways(1)
        self.rect.move_ip(0,-self.ymoment)
        __ = pygame.sprite.spritecollideany(self,terrain_sprites)
        if not __ is None:
            if self.rect.top + self.ymoment > __.rect.bottom:
                self.rect.top = __.rect.bottom
                self.ymoment = 0
                self.ymoment -=1 if not self.jumping else 0.75
                self.falling = True
            else:
                self.ymoment = 0
                self.falling = False
                self.rect.bottom = __.rect.top
        else: 
            self.ymoment -=1 if not self.jumping else 0.75
            self.falling = True
        try: pygame.sprite.spritecollideany(self,portal_sprites).changelevel()
        except: pass
    def movecheck(self,direction):
        self.rect.move_ip(direction,0)
        __ = pygame.sprite.spritecollideany(self,terrain_sprites)
        if not __ is None:
            if direction>0:
                self.rect.right = __.rect.left
                self.wj = True
            else:
                self.rect.left = __.rect.right
                self.wj = True
        else: 
            self.wj = False
            pass

class terrainsprites(pygame.sprite.Sprite):
    def __init__(self, color_,coords, width,height) -> None:
        super().__init__()
        self.image = pygame.Surface([width,height])
        pygame.draw.rect(self.image,color_,pygame.Rect(0,0,width,height))
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]    
class portalsprites(pygame.sprite.Sprite):
    def __init__(self, color_,coords, width,height,level) -> None:
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.rect = self.image.get_rect()
        self.interact = level
        pygame.draw.rect(self.image,color_,pygame.Rect(0,0,width,height))
        self.rect.x = coords[0]
        self.rect.y = coords[1]
    def changelevel(self):
        if self.interact ==0:Levels.build(0)
        elif self.interact ==1:Levels.build(1)

def draw_rect_alpha(surface,rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf,(255,255,255,1),shape_surf.get_rect())
    surface.blit(shape_surf,rect)

class Levels():
    def __init__(self) -> None:
        self.w = (255,255,255)
        self.p = (255,127.5,255)
        self.g = (0,255,0)
        self.coord = [(screensize[0]/2,screensize[1]*9/10),(screensize[0]/2,screensize[1]*9/10)]
        self.pw = screensize[0]/40
        self.ph = screensize[1]/5
    def reset(self,coords:tuple[float,float]):
        terrain_sprites.empty()
        portal_sprites.empty()
        object_.rect.centerx = coords[0]
        object_.rect.bottom = coords[1]
    def build(self,num):
        self.reset(self.coord[num])
        self.create(num)
    def create(self,num):
        for i in range(0,len(lvlsobj["levels"][0][str(num)]["t"])):
            terrain_sprites.add(terrainsprites((float(lvlsobj["levels"][0]["0"]["t"][str(i)]["c"]["r"]),float(lvlsobj["levels"][0]["0"]["t"][str(i)]["c"]["g"]),float(lvlsobj["levels"][0]["0"]["t"][str(i)]["c"]["b"]))\
                ,(self.interpret(lvlsobj["levels"][0]["0"]["t"][str(i)]["l"]["x"]),self.interpret(lvlsobj["levels"][0]["0"]["t"][str(i)]["l"]["y"]))\
                    ,self.interpret(lvlsobj["levels"][0]["0"]["t"][str(i)]["h"])\
                        ,self.interpret(lvlsobj["levels"][0]["0"]["t"][str(i)]["w"])))
        for i in range(0,len(lvlsobj["levels"][0][str(num)]["p"])):
            portal_sprites.add(portalsprites((float(lvlsobj["levels"][0]["0"]["p"][str(i)]["c"]["r"]),float(lvlsobj["levels"][0]["0"]["p"][str(i)]["c"]["g"]),float(lvlsobj["levels"][0]["0"]["p"][str(i)]["c"]["b"]))\
                ,(self.interpret(lvlsobj["levels"][0]["0"]["p"][str(i)]["l"]["x"]),self.interpret(lvlsobj["levels"][0]["0"]["p"][str(i)]["l"]["y"]))\
                    ,self.interpret(lvlsobj["levels"][0]["0"]["p"][str(i)]["h"])\
                        ,self.interpret(lvlsobj["levels"][0]["0"]["p"][str(i)]["w"])\
                            ,int(lvlsobj["levels"][0]["0"]["p"][str(i)]["le"])))
    def interpret(self,string:str):
        s = list(string)
        p = []
        for i in range(0,len(s)):
            if s[i] == "s": s[i] = str(screensize[0])
            if s[i] == "d": s[i] = str(screensize[1])
        for i in range(0,len(s)):
            if i > len(s) - 1: break
            if s[i] == "*": 
                p = []
                if i > 1:
                    for j in range(0,i-1):
                        p.append(s[j])
                p.append(str(int(s[i-1])*int(s[i+1])))
                if len(s) - i > 2:
                    for j in range(i+2,len(s) - 1):
                        p.append(s[j])
                s=p
            if s[i] == "/": 
                p = []
                if i > 1:
                    for j in range(0,i-1):
                        p.append(s[j])
                p.append(str(int(s[i-1])/int(s[i+1])))
                if len(s) - i > 2:
                    for j in range(i+2,len(s) - 1):
                        p.append(s[j])
                s=p
        for i in range(0,len(s)):
            if s[i] == "+": 
                p = []
                if i > 1:
                    for j in range(0,i-1):
                        p.append(s[j])
                p.append(str(int(s[i-1])+int(s[i+1])))
                if len(s) - i > 2:
                    for j in range(i+2,len(s) - 1):
                        p.append(s[j])
                s=p
            if s[i] == "-": 
                p = []
                if i > 1:
                    for j in range(0,i-1):
                        p.append(s[j])
                p.append(str(int(s[i-1])-int(s[i+1])))
                if len(s) - i > 2:
                    for j in range(i+2,len(s) - 1):
                        p.append(s[j])
                s=p
        return int(float(s[0]))
terrain_sprites = pygame.sprite.Group()
portal_sprites = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

object_ = Sprite(white,100,100)
object_.rect.x = screen.get_width()/2
object_.rect.y = screen.get_height()/2
all_sprites_list.add(object_)
levels = Levels()
levels.build(0)


        

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    object_.move()
    all_sprites_list.update()
    screen.fill((0,0,0))
    terrain_sprites.draw(screen)
    portal_sprites.draw(screen)
    all_sprites_list.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()