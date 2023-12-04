import pygame
from pygame.locals import *
import pygame.gfxdraw
import random
import math

from pygame.sprite import AbstractGroup

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
        self.oheight = height
        self.owidth = width
        self.adheight = height
        self.adwidth = width
        self.progression = 0
        self.colour = colour
        self.rs = [1/16,1/8,1/2,3/4,15/16,7/16,14/16]
        self.degs = [random.randrange(0,360) for _ in range(0,7)]
        self.jumping = False
        self.crouching = False
        self.ymoment = 0
        
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
        self.adwidth = self.owidth
        self.adheight = self.adwidth
        self.image = pygame.Surface([self.adwidth,self.adheight])
        self.image.fill((0,0,0,0))
        self.progression +=5*direction*-1
        if self.progression > 359: self.progression = 0
        pygame.gfxdraw.filled_circle(self.image,int(round(self.adwidth/2)),int(round(self.adheight/2)),int(round(self.adwidth/2)),(self.colour[0]-20 if self.colour[0]>19 else 0,self.colour[1]-20 if self.colour[1]>19 else 0,self.colour[2]-20 if self.colour[2]>19 else 0))
        pygame.gfxdraw.circle(self.image,int(round(self.adheight/2)),int(round(self.adheight/2)),int(round(self.adwidth/2)),self.colour)
        try: s
        except NameError: s=0
        if self.progression % 20 == 0: s = random.randrange(0,31)
        for i in range(0,7):
            pygame.draw.arc(self.image,self.colour,Rect(int(round((self.adheight-self.adheight*self.rs[i])/2)),int(round((self.adheight-self.adheight*self.rs[i])/2)),int(round(self.adheight*self.rs[i])),int(round(self.adheight*self.rs[i]))),math.radians(self.progression+self.degs[i]),math.radians(self.progression+self.degs[i]+15+s),int(round(self.adwidth/2/15)))      
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_w] or pressed_keys[K_SPACE]:
            self.jumping = True
            self.rect.move_ip(0, -5)
        if pressed_keys[K_s]:
            self.crouching = True
            self.rect.move_ip(0,5)
        if pressed_keys[K_a]:
            if self.rect.left > 0:
                self.rect.move_ip(-5, 0)
                if not self.jumping: self.movesideways(-1)
        if pressed_keys[K_d]:
            if self.rect.right < screen.get_width():
                self.rect.move_ip(5, 0)
                if not self.jumping: self.movesideways(1)

class terrainsprites(pygame.sprite.Sprite):
    def __init__(self, color, width,height) -> None:
        super().__init__()
        self.image = pygame.Surface([width,height])
        pygame.draw.rect(self.image,color,pygame.Rect(0,0,width,height))
        
class portalsprites(pygame.sprite.Sprite):
    def __init__(self, color,coords, width,height,level) -> None:
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.interact = level
        pygame.draw.rect(self.image,color,pygame.Rect(0,0,width,height))
    def changelevel(self):
        if self.interact ==0:Levels.start()
        elif self.interact ==1:Levels.one()

class Levels:
    def reset(self,coords:tuple[int,int]):
        terrain_sprites.empty()
        screen.fill((0,0,0))
        object_.rect.x = coords[0]
        object_.rect.y = coords[1]
    def start(self):
        self.reset((screensize[0]/2,screensize[1]/2))
        portal_sprites.add(portalsprites((255,255,255),(0,0),10,20,1))
    def one(self):
        self.reset((screensize[0]/2,screensize[1]/2))

terrain_sprites = pygame.sprite.Group()
portal_sprites = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

object_ = Sprite(white,100,100)
object_.rect.x = screen.get_width()/2
object_.rect.y = screen.get_height()/2
all_sprites_list.add(object_)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if not pygame.sprite.spritecollideany(object_,)
    object_.move()
    all_sprites_list.update()
    screen.fill((0,0,0))
    all_sprites_list.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()