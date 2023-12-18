import pygame
from pygame.locals import *
import pygame.gfxdraw
import random
import math
import json

with open("levels.json", "r") as read:
    lvlsobj = json.load(read)
pygame.init()
FPS = 60
clock = pygame.time.Clock()
screensize = (1280, 720)
screen = pygame.display.set_mode(screensize)
running = True
white = (255, 255, 255)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, colour, height, width) -> None:
        super().__init__()
        self.jnm = True
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
        self.rs = [i/12 for i in range(1, 12)]
        self.degs = [random.randrange(0, 360) for _ in range(0, len(self.rs))]
        self.jumping = False
        self.crouching = False
        self.ymoment = 0
        self.startofjump = 0
        self.falling = False

        head_width = width/5
        head_height = height/4
        shoulder_height = height/8
        arm_width = width/5
        body_width = width/2
        legs_height = height*5/16
        body_height = height-(head_height+shoulder_height+legs_height)

        self.image = pygame.Surface([width, height],pygame.SRCALPHA)
        # head
        pygame.draw.rect(self.image, colour, pygame.Rect(
            (width-head_width)/2, 0, head_width, head_height))
        # shoulders
        pygame.draw.rect(self.image, colour, pygame.Rect(
            0, head_height, width, shoulder_height))
        # arms
        pygame.draw.rect(self.image, colour, pygame.Rect(
            0, head_height+shoulder_height, arm_width, body_height))
        pygame.draw.rect(self.image, colour, pygame.Rect(
            width-arm_width, head_height+shoulder_height, arm_width, body_height))
        # body
        pygame.draw.rect(self.image, colour, pygame.Rect(
            (width-body_width)/2, head_height+shoulder_height, body_width, body_height))
        # legs
        pygame.draw.rect(self.image, colour, pygame.Rect(
            (width-body_width)/2, head_height+shoulder_height+body_height, body_width*7/16, legs_height))
        pygame.draw.rect(self.image, colour, pygame.Rect((width-body_width)/2+body_width *
                         9/16, head_height+shoulder_height+body_height, body_width*7/16+1, legs_height))

        self.rect = self.image.get_rect()
        self.rect.width = self.adwidth
        self.rect.height = self.adheight

    def movesideways(self, direction):
        if self.jnm:
            self.rect.move_ip(0,self.adheight - self.owidth * self.adjustmentw)
            self.adwidth = self.owidth * self.adjustmentw
            self.adheight = self.owidth * self.adjustmentw
            self.image = pygame.Surface([self.adwidth, self.adwidth],pygame.SRCALPHA)
            self.rect.width = self.adwidth
            self.rect.height = self.adwidth
            self.jnm = False
        self.image.fill((255, 255, 255, 0))
        self.progression += 10*direction*-1
        if self.progression > 359:
            self.progression = 0
        adjusted_colour = (
            255-self.colour[0], 255-self.colour[1], 255-self.colour[2])
        pygame.gfxdraw.filled_circle(self.image, int(
            self.adwidth/2), int(self.adheight/2), int(self.adwidth/2), self.colour)
        pygame.gfxdraw.circle(self.image, int(self.adwidth/2), int(
            self.adheight/2), int(self.adwidth/2), self.colour)
        try:
            s
        except NameError:
            s = 0
        if self.progression % 20 == 0:
            s = random.randrange(0, 5)
        for i in range(0, len(self.rs)):
            pygame.draw.arc(self.image, adjusted_colour, 
                            Rect(int((self.adwidth-self.adwidth*self.rs[i])/2), int((self.adheight-self.adheight*self.rs[i])/2), int(self.adwidth*self.rs[i]), int(self.adheight*self.rs[i])), 
                            math.radians(self.progression+self.degs[i]), math.radians(self.progression+self.degs[i]+45+s), int(round(self.adwidth/2/15)))

    def jump(self):
        if not self.jnm:
            self.rect.move_ip(0,self.adheight - self.oheight * self.adjustmenth)
            self.adheight = self.oheight * self.adjustmenth
            self.adwidth = self.owidth * self.adjustmentw 
            self.image = pygame.Surface([self.adwidth, self.adheight],pygame.SRCALPHA)
            self.rect.width = self.adwidth
            self.rect.height = self.adheight
            self.jnm = True
        self.image.fill((255, 255, 255, 0))
        head_width = self.adwidth/5
        head_height = self.adheight/4
        shoulder_height = self.adheight/8
        arm_width = self.adwidth/5
        body_width = self.adwidth/2
        legs_height = self.adheight*5/16
        body_height = self.adheight-(head_height+shoulder_height+legs_height)
        # head
        pygame.draw.rect(self.image, self.colour, pygame.Rect(
            (self.adwidth-head_width)/2, 0, head_width, head_height))
        # shoulders
        pygame.draw.rect(self.image, self.colour, pygame.Rect(
            0, head_height, self.adwidth, shoulder_height))
        # arms
        pygame.draw.rect(self.image, self.colour, pygame.Rect(
            0, head_height+shoulder_height, arm_width, body_height))
        pygame.draw.rect(self.image, self.colour, pygame.Rect(
            self.adwidth-arm_width, head_height+shoulder_height, arm_width, body_height))
        # body
        pygame.draw.rect(self.image, self.colour, pygame.Rect(
            (self.adwidth-body_width)/2, head_height+shoulder_height, body_width, body_height))
        # legs
        pygame.draw.rect(self.image, self.colour, pygame.Rect(
            (self.adwidth-body_width)/2, head_height+shoulder_height+body_height, body_width*7/16, legs_height))
        pygame.draw.rect(self.image, self.colour, pygame.Rect((self.adwidth-body_width)/2+body_width *
                         9/16, head_height+shoulder_height+body_height, body_width*7/16+1, legs_height))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LSHIFT]:
            self.sprint = True
        else:
            self.sprint = False
        if pressed_keys[K_w] or pressed_keys[K_SPACE]:
            self.jump()
            self.jumping = True
            if not self.falling:
                self.ymoment = 17
            if self.wj and pygame.time.get_ticks()-self.startofjump > 300:
                self.startofjump = pygame.time.get_ticks()
                self.ymoment = 20
        else:
            self.jumping = False
        if pressed_keys[K_s]:
            self.crouching = True
        if pressed_keys[K_a]:
            if self.rect.left > 0:
                self.movecheck(-8 if self.sprint else -5)
                if not self.falling:
                    self.movesideways(-1)
        if pressed_keys[K_d]:
            if self.rect.right < screensize[0]:
                self.movecheck(8 if self.sprint else 5)
                if not self.falling:
                    self.movesideways(1)
        self.rect.move_ip(0, -self.ymoment)
        __ = pygame.sprite.spritecollideany(self, terrain_sprites)
        if not __ is None:
            if self.rect.top + self.ymoment > __.rect.bottom:
                self.rect.top = __.rect.bottom
                self.ymoment = 0
                self.ymoment -= 1 if not self.jumping else 0.75
                self.falling = True
            else:
                self.ymoment = 0
                self.falling = False
                self.rect.bottom = __.rect.top
        else:
            self.ymoment -= 1 if not self.jumping else 0.75
            self.falling = True
        try:
            pygame.sprite.spritecollideany(self, portal_sprites).changelevel()
        except:
            pass
        if self.rect.bottom > screensize[1]:
            levels.build(levels.CL)

    def movecheck(self, direction):
        self.rect.move_ip(direction, 0)
        __ = pygame.sprite.spritecollideany(self, terrain_sprites)
        if not __ is None:
            if direction > 0:
                self.rect.right = __.rect.left
            elif direction < 0:
                self.rect.left = __.rect.right
            self.wj = True
        else:
            self.wj = False

class terrainsprites(pygame.sprite.Sprite):
    def __init__(self, color_, coords, width, height) -> None:
        super().__init__()
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color_, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]


class portalsprites(pygame.sprite.Sprite):
    def __init__(self, color_, coords, width, height, level) -> None:
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.interact = level
        pygame.draw.rect(self.image, color_, pygame.Rect(0, 0, width, height))
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def changelevel(self):
        levels.build(self.interact)
        levels.CL = self.interact

class Levels():
    def __init__(self) -> None:
        self.coord = [(screensize[0]/10, screensize[1]*9/10),
                      (screensize[0]/2, screensize[1]*9/10),
                      (10,10)]
        self.CL = 0

    def reset(self, coords: tuple[float, float]):
        terrain_sprites.empty()
        portal_sprites.empty()
        object_.rect.centerx = coords[0]
        object_.rect.bottom = coords[1]

    def build(self, num):
        self.reset(self.coord[num])
        self.create(num)

    def create(self, num):
        _t = lvlsobj["levels"][num]["t"]
        for i in range(0, len(_t)):
            terrain_sprites.add(terrainsprites((float(_t[i]["c"][0]), float(_t[i]["c"][1]), float(_t[i]["c"][2])), (self.interpret(
                _t[i]["l"]["x"]), self.interpret(_t[i]["l"]["y"])), self.interpret(_t[i]["h"]), self.interpret(_t[i]["w"])))
        _p = lvlsobj["levels"][num]["p"]
        for i in range(0, len(_p)):
            portal_sprites.add(portalsprites((float(_p[i]["c"][0]), float(_p[i]["c"][1]), float(_p[i]["c"][2])), (self.interpret(
                _p[i]["l"]["x"]), self.interpret(_p[i]["l"]["y"])), self.interpret(_p[i]["h"]), self.interpret(_p[i]["w"]),int(_p[i]["le"])))

    def interpret(self, string: str):
        s = string.split(" ")
        for i in range(0, len(s)):
            if s[i] == "s":
                s[i] = str(screensize[0])
            if s[i] == "d":
                s[i] = str(screensize[1])
        while (len(s) > 1 and("*"in s or "/"in s)):
            for i in range(0, len(s)):
                if s[i] == "*":
                    s[i] = str(float(s[i-1])*float(s[i+1]))
                    a = [s[i-1],s[i+1]]
                    s.remove(a[0])
                    s.remove(a[1])
                    break
                if s[i] == "/":
                    s[i] = str(float(s[i-1])/float(s[i+1]))
                    a = [s[i-1],s[i+1]]
                    s.remove(a[0])
                    s.remove(a[1])
                    break
        while (len(s) > 1):
            for i in range(0, len(s)):
                if s[i] == "+":
                    s[i] = str(float(s[i-1])+float(s[i+1]))
                    a = [s[i-1],s[i+1]]
                    s.remove(a[0])
                    s.remove(a[1])
                    break
                if s[i] == "-":
                    s[i] = str(float(s[i-1]) - float(s[i+1]))
                    a = [s[i-1],s[i+1]]
                    s.remove(a[0])
                    s.remove(a[1])
                    break
        return int(float(s[0]))


terrain_sprites = pygame.sprite.Group()
portal_sprites = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

object_ = Sprite(white, 100, 80)
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
    screen.fill((0, 0, 0))
    terrain_sprites.draw(screen)
    portal_sprites.draw(screen)
    all_sprites_list.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
