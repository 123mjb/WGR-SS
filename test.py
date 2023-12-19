import time
import pygame
from pygame.locals import *
import pygame.gfxdraw
import json

with open("levels.json", "r") as read:
    lvlsobj = json.load(read)
    
pygame.init()
FPS = 60
clock = pygame.time.Clock()
screensize = (1280, 720)
screen = pygame.display.set_mode(screensize)
running = True

class terrainsprites(pygame.sprite.Sprite):
    def __init__(self, color_, coords, width, height) -> None:
        super().__init__()
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color_, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        
class portalsprites(pygame.sprite.Sprite):
    def __init__(self, color_:tuple, coords, width, height, level) -> None:
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.interact = level
        pygame.draw.rect(self.image, color_, pygame.Rect(0, 0, width, height))
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def changelevel(self):
        if self.interact == 0:
            levels.build(0)
        elif self.interact == 1:
            levels.build(1)
            
class Levels():
    def __init__(self) -> None:
        self.coord = [(screensize[0]/2, screensize[1]*9/10),
                      (screensize[0]/2, screensize[1]*9/10)]
        self.pw = screensize[0]/40
        self.ph = screensize[1]/5

    def reset(self):
        terrain_sprites.empty()
        portal_sprites.empty()
        spike_sprites.empty()

    def build(self, num):
        self.reset()
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
        _s = lvlsobj["levels"][num]["s"]
        if len(_s)>0:
            for i in range(0, len(_s)):
                for j in range(0,5):
                    spike_sprites.add(Deathsprites((float(_s[i]["c"][0]), float(_s[i]["c"][1]), float(_s[i]["c"][2])), 
                                                   (int(round(( self.interpret(_s[i]["l"]["x"]) + self.interpret(_s[i]["h"]) * (1-(j + 1)/6)/2))), 
                                                    int(round(( self.interpret(_s[i]["l"]["y"]) + self.interpret(_s[i]["w"]) * (1-((5-j) + 1)/6)/2)))), 
                                                   self.interpret(_s[i]["h"]) * (j + 1)/6, 
                                                   self.interpret(_s[i]["w"])/6))

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
spike_sprites = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

levels = Levels()
levels.build(0)
level = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_0]:
        level = 0
    if pressed_keys[K_1]:
        level = 1
    if pressed_keys[K_2]:
        level = 2
    with open("levels.json", "r") as read:
        lvlsobj = json.load(read)
    levels.build(level)
    all_sprites_list.update()
    screen.fill((0, 0, 0))
    terrain_sprites.draw(screen)
    portal_sprites.draw(screen)
    spike_sprites.draw(screen)
    all_sprites_list.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
    time.sleep(2)
pygame.quit()