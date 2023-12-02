import pygame
from pygame.locals import *
import pygame.gfxdraw
import random
import math

pygame.init()
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720))
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
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
        if pressed_keys[K_a]:
            if self.rect.left > 0:
                self.rect.move_ip(-5, 0)
                self.movesideways(-1)
        if pressed_keys[K_d]:
            if self.rect.right < screen.get_width():
                self.rect.move_ip(5, 0)
                self.movesideways(1)
        
all_sprites_list = pygame.sprite.Group()

object_ = Sprite(white,200,200)
object_.rect.x = screen.get_width()
object_.rect.y = screen.get_height()/2

all_sprites_list.add(object_)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    object_.move()
    all_sprites_list.update()
    screen.fill((0,0,0))
    all_sprites_list.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()