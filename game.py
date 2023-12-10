import pygame
from pygame.locals import *
import pygame.gfxdraw
import random
import math

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
        self.adjustmenth = 1
        self.adjustmentw = 1
        self.progression = 0
        self.colour = colour
        self.rs = [1/16,1/8,1/2,3/4,15/16,7/16,14/16]
        self.degs = [random.randrange(0,360) for _ in range(0,7)]
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
        self.progression +=5*direction*-1
        if self.progression > 359: self.progression = 0
        pygame.gfxdraw.filled_circle(self.image,int(round(self.adwidth/2)),int(round(self.adheight/2)),int(round(self.adwidth/2)),(self.colour[0]-20 if self.colour[0]>19 else 0,self.colour[1]-20 if self.colour[1]>19 else 0,self.colour[2]-20 if self.colour[2]>19 else 0))
        pygame.gfxdraw.circle(self.image,int(round(self.adheight/2)),int(round(self.adheight/2)),int(round(self.adwidth/2)),self.colour)
        try: s
        except NameError: s=0
        if self.progression % 20 == 0: s = random.randrange(0,31)
        for i in range(0,7):
            pygame.draw.arc(self.image,self.colour,Rect(int(round((self.adheight-self.adheight*self.rs[i])/2)),int(round((self.adheight-self.adheight*self.rs[i])/2)),int(round(self.adheight*self.rs[i])),int(round(self.adheight*self.rs[i]))),math.radians(self.progression+self.degs[i]),math.radians(self.progression+self.degs[i]+15+s),int(round(self.adwidth/2/15)))      
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
        """_ = pygame.sprite.spritecollideany(self,terrain_sprites)
        if _ is None:
            self.falling = True
            self.ymoment -= 1
        else:
            if self.rect.top > _.rect.top:
                pass
            elif self.rect.bottom < _.rect.bottom:
                self.rect.bottom = _.rect.top + 1
                self.ymoment = 0
                self.falling = False
            else:
                self.ymoment = 0
                self.falling = False"""
        
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_w] or pressed_keys[K_SPACE]:
            self.jump()
            self.jumping = True
            if not self.falling:
                self.ymoment = 15
        else: self.jumping = False
        if pressed_keys[K_s]:
            self.crouching = True
        if pressed_keys[K_a]:
            if self.rect.left > 0:
                self.movecheck(-5)
                if not self.falling: self.movesideways(-1)
        if pressed_keys[K_d]:
            if self.rect.right < screen.get_width():
                self.movecheck(5)
                if not self.falling: self.movesideways(1)
        self.rect.move_ip(0,-self.ymoment)
        __ = pygame.sprite.spritecollideany(self,terrain_sprites)
        if not __ is None:
            self.ymoment = 0
            self.falling = False
            self.rect.bottom = __.rect.top
        else: 
            self.ymoment -=1
            self.falling = True
    def movecheck(self,direction):
        self.rect.move_ip(direction,0)
        __ = pygame.sprite.spritecollideany(self,terrain_sprites)
        if not __ is None:
            if direction>0:
                self.rect.right = __.rect.left
            else:
                self.rect.left = __.rect.right
        else: 
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
        if self.interact ==0:levels.start()
        elif self.interact ==1:levels.one()

def draw_rect_alpha(surface,rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf,(255,255,255,1),shape_surf.get_rect())
    surface.blit(shape_surf,rect)

class Levels():
    def __init__(self) -> None:
        pass
    def reset(self,coords:tuple[int,int]):
        terrain_sprites.empty()
        object_.rect.x = coords[0]
        object_.rect.y = coords[1]
    def start(self):
        self.reset((screensize[0]/2,screensize[1]/2))
        terrain_sprites.add(terrainsprites((255,255,255),(0,screensize[1] - screensize[1]/10),screensize[0],screensize[1]/10))
        portal_sprites.add(portalsprites((255,255,255),(0,screensize[1] - screensize[1]/5),screensize[0]/20,screensize[1]/5,1))
    def one(self):
        self.reset((screensize[0]/2,screensize[1]/2))
        terrain_sprites.add(terrainsprites((255,255,255),(0,screensize[1] - screensize[1]/10),screensize[0],screensize[1]/10))
        portal_sprites.add(portalsprites((255,255,255),(0,screensize[1] - screensize[1]/5),screensize[0]/20,screensize[1]/5,0))

terrain_sprites = pygame.sprite.Group()
portal_sprites = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

object_ = Sprite(white,100,100)
object_.rect.x = screen.get_width()/2
object_.rect.y = screen.get_height()/2
all_sprites_list.add(object_)
levels = Levels()
levels.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    try: pygame.sprite.spritecollideany(object_,portal_sprites).changelevel()
    except: pass
    object_.move()
    all_sprites_list.update()
    screen.fill((0,0,0))
    terrain_sprites.draw(screen)
    portal_sprites.draw(screen)
    all_sprites_list.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()