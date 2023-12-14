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
    def __init__(self, color_, coords, width, height, level) -> None:
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

    def reset(self, coords: tuple[float, float]):
        terrain_sprites.empty()
        portal_sprites.empty()

    def build(self, num):
        self.reset(self.coord[num])
        self.create(num)

    def create(self, num):
        for i in range(0, len(lvlsobj["levels"][num][str(num)]["t"])):
            terrain_sprites.add(terrainsprites((float(lvlsobj["levels"][num][str(num)]["t"][str(i)]["c"]["r"]), float(lvlsobj["levels"][num][str(num)]["t"][str(i)]["c"]["g"]), float(lvlsobj["levels"][num][str(num)]["t"][str(i)]["c"]["b"])), (self.interpret(
                lvlsobj["levels"][num][str(num)]["t"][str(i)]["l"]["x"]), self.interpret(lvlsobj["levels"][num][str(num)]["t"][str(i)]["l"]["y"])), self.interpret(lvlsobj["levels"][num][str(num)]["t"][str(i)]["h"]), self.interpret(lvlsobj["levels"][num][str(num)]["t"][str(i)]["w"])))
        for i in range(0, len(lvlsobj["levels"][num][str(num)]["p"])):
            portal_sprites.add(portalsprites((float(lvlsobj["levels"][num][str(num)]["p"][str(i)]["c"]["r"]), float(lvlsobj["levels"][num][str(num)]["p"][str(i)]["c"]["g"]), float(lvlsobj["levels"][num][str(num)]["p"][str(i)]["c"]["b"])), (self.interpret(
                lvlsobj["levels"][num][str(num)]["p"][str(i)]["l"]["x"]), self.interpret(lvlsobj["levels"][num][str(num)]["p"][str(i)]["l"]["y"])), self.interpret(lvlsobj["levels"][num][str(num)]["p"][str(i)]["h"]), self.interpret(lvlsobj["levels"][num][str(num)]["p"][str(i)]["w"]),int(lvlsobj["levels"][num][str(num)]["p"][str(i)]["le"])))

    def interpret(self, string: str):
        s = list(string)
        for i in range(0, len(s)):
            if s[i] == "s":
                s[i] = str(screensize[0])
            if s[i] == "d":
                s[i] = str(screensize[1])
        while (len(s) > 1 and("*"in s or "/"in s)):
            for i in range(0, len(s)):
                if s[i] == "*":
                    s[i] = str(float(s[i-1])*float(s[i+1]))
                    s.remove(s[i+1])
                    s.remove(s[i-1])
                    break
                if s[i] == "/":
                    s[i] = str(float(s[i-1])/float(s[i+1]))
                    s.remove(s[i+1])
                    s.remove(s[i-1])
                    break
        while (len(s) > 1):
            for i in range(0, len(s)):
                if s[i] == "+":
                    s[i] = str(float(s[i-1])+float(s[i+1]))
                    s.remove(s[i+1])
                    s.remove(s[i-1])
                    break
                if s[i] == "-":
                    s[i] = str(float(s[i-1])-float(s[i+1]))
                    s.remove(s[i+1])
                    s.remove(s[i-1])
                    break
        return int(float(s[0]))
    
terrain_sprites = pygame.sprite.Group()
portal_sprites = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

levels = Levels()
levels.build(0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    with open("levels.json", "r") as read:
        lvlsobj = json.load(read)
    levels.build(0)
    all_sprites_list.update()
    screen.fill((0, 0, 0))
    terrain_sprites.draw(screen)
    portal_sprites.draw(screen)
    all_sprites_list.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
    time.sleep(2)
pygame.quit()