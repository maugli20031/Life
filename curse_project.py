import pygame, sys
from pygame.locals import *
import random

shirina = 300
visota = 300
razmer = 10

assert shirina % razmer == 0, "izmenite razmer of screen"
assert visota % razmer == 0, "izmenite razmer of screen"

Allinwidth = shirina // razmer
Allinhigh = visota // razmer

def MakeThemDead():
    shotoTam = {}
    for y in range (Allinhigh):
        for x in range (Allinwidth):
            shotoTam[x,y] = 0
    return shotoTam

def MakeSomeAlive(aLife):
    for mesto in aLife:
        aLife[mesto] = random.randint(0,1)
    return aLife

black =    (0,  0,  0)
white =    (255,255,255)
gray = (40, 40, 40)
alive =    (110,  100, 40)

def MakeSomeGrid():
    for x in range(0, shirina, razmer):
        pygame.draw.line(dispshow, gray, (x,0),(x,visota))
    for y in range (0, visota, razmer):
        pygame.draw.line(dispshow, gray, (0,y), (shirina, y))

FPS = 10

def ShowThem(mesto, aLife, timer):
    x = mesto[0]
    y = mesto[1]
    y = y * razmer
    x = x * razmer
    if aLife[mesto] >= 1:
        pygame.draw.rect(dispshow, alive, (x, y, razmer, razmer))
        aLife[mesto] = 1
        timer[mesto] += 0.1
    if aLife[mesto] == 0 or timer[mesto] >= 10:
        pygame.draw.rect(dispshow, white, (x, y, razmer, razmer))
        aLife[mesto] = 0
        timer[mesto] = 0
    return None

def frame(aLife, timer):
    newFrame = {}
    for mesto in aLife:
        sosed = Count_A_Bit(mesto, aLife)
        if aLife[mesto] >= 1:
            if sosed >= 6 or timer[mesto] >= 10:
                newFrame[mesto] = 0
            else:
                newFrame[mesto] = 1
        elif aLife[mesto] == 0:
            if sosed == 2:
                newFrame[mesto] = 1
            else:
                newFrame[mesto] = 0
        else:
            newFrame[mesto] = 0
    return newFrame

def Count_A_Bit(mesto,aLife):
    sosed = 0
    for x in range (-1,2):
        for y in range (-1,2):
            proverka = (mesto[0]+x,mesto[1]+y)
            if proverka[0] < Allinwidth  and proverka[0] >=0:
                if proverka [1] < Allinhigh and proverka[1]>= 0:
                    if aLife[proverka] >= 1:
                        if x == 0 and y == 0:
                            sosed += 0
                        else:
                            sosed += 1
    return sosed

def main():
    pygame.init()
    global dispshow
    FpS = pygame.time.Clock()
    dispshow = pygame.display.set_mode((shirina,visota))
    pygame.display.set_caption('Game Of Life')
    dispshow.fill(white)
    timer = MakeThemDead()
    aLife = MakeThemDead()
    aLife = MakeSomeAlive(aLife)
    for mesto in aLife:
        ShowThem(mesto, aLife, timer)
    MakeSomeGrid()
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        aLife = frame(aLife, timer)
        for mesto in aLife:
            ShowThem(mesto, aLife, timer)
        MakeSomeGrid()
        pygame.display.update()
        FpS.tick(FPS)

if __name__=='__main__':
    main()
