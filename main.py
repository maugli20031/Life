import pygame, sys
from pygame.locals import *
import random

FPS = 10 #На нем висит скорость развития колонии

WINDOWWIDTH = 600 #ширина окна, влияет на количество клеток в ширину
WINDOWHEIGHT = 600 #высота окна, влияет на количество клеток в высоту
CELLSIZE = 20 #размер клетки
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"

CELLWIDTH = WINDOWWIDTH // CELLSIZE #получаем int количесвта клеток, чтобы поровну распределить на площади
CELLHEIGHT = WINDOWHEIGHT // CELLSIZE

#определяем цвета в RGB, можно менять
BLACK =    (0,  0,  0)
WHITE =    (255,255,255)
DARKGRAY = (40, 40, 40)
GREEN =    (0,  255,0)

#Отрисовка решетки
def Grider():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x,0),(x,WINDOWHEIGHT))
    for y in range (0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0,y), (WINDOWWIDTH, y))

#заполняем клетки
def kletki():
    gridDict = {}
    for y in range (CELLHEIGHT):
        for x in range (CELLWIDTH):
            gridDict[x,y] = 0
    return gridDict

#а теперь заполняем их рандомной жизнью
def RandomFill(life):
    for item in life:
        life[item] = random.randint(0,1)
    return life

#красим живых в зеленый
def colourise(item, life):
    x = item[0]
    y = item[1]
    y = y * CELLSIZE
    x = x * CELLSIZE
    if life[item] == 0:
        pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, CELLSIZE, CELLSIZE))
    if life[item] == 1:
        pygame.draw.rect(DISPLAYSURF, GREEN, (x, y, CELLSIZE, CELLSIZE))
    return None

#получаем информацию о соседях клетки
def Neighbour(item,life):
    neighbours = 0
    for x in range (-1,2):
        for y in range (-1,2):
            checkCell = (item[0]+x,item[1]+y)
            if checkCell[0] < CELLWIDTH  and checkCell[0] >=0:
                if checkCell [1] < CELLHEIGHT and checkCell[1]>= 0:
                    if life[checkCell] == 1:
                        if x == 0 and y == 0:
                            neighbours += 0
                        else:
                            neighbours += 1
    return neighbours

#высчитываем потенциал клетки, можно менять абсолютно все ради динамики,
#не стал делать смерть от 6 клеток соседей, так как в таком случае колония не двигается
def tick(life):
    newTick = {}
    for item in life:
        numberNeighbours = Neighbour(item, life)
        if life[item] == 1:
            if numberNeighbours < 2:
                newTick[item] = 0
            elif numberNeighbours > 2:
                newTick[item] = 0
            else:
                newTick[item] = 1
        elif life[item] == 0:
            if numberNeighbours == 2:
                newTick[item] = 1
            else:
                newTick[item] = 0
    return newTick

#главная функция, отрисовка всего и обновление экрана для дальнейшей отрисовки
def main():
    pygame.init()
    global DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Life')
    DISPLAYSURF.fill(WHITE)
    life = kletki()
    life = RandomFill(life)
    for item in life:
        colourise(item, life)
    Grider()
    pygame.display.update()

    while True: #вот здесь главный цикл, время и распределение цвета
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        life = tick(life)
        for item in life:
            colourise(item, life)
        Grider()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
