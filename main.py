import random

import pygame
from datetime import datetime

from constants import *

class Game(object):

    def __init__(self):
        super().__init__()
        self.surface: pygame.Surface = None
        self.__running = False
        self.cells = [] # 0=dead, 1=alive

    def init_game(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__running = True
        self.__init_cells()


    def run(self):
        MS_PER_UPDATE = 60 / 1000
        last_time = datetime.now().timestamp()
        lag = 0

        while self.__running:
            current_time = datetime.now().timestamp()
            elapsed = current_time - last_time
            lag += elapsed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()
                    return
            
            while lag >= MS_PER_UPDATE:
                self.__update()
                lag -= MS_PER_UPDATE
            self.__render()
            pygame.display.flip()

            last_time = current_time


    def __update(self):
        for y in range(int(HEIGHT/CH)):
            for x in range(int(WIDTH/CW)):
                ul = um = ur = ml = mr = ll = \
                    lm = lr = 0
                if y > 0:
                    if x > 0:
                        ul = self.cells[y-1][x-1]
                    um = self.cells[y-1][x]
                    if x < (WIDTH/CW)-1:
                        ur = self.cells[y-1][x+1]

                if x > 0:
                    ml = self.cells[y][x-1]
                if x < (WIDTH/CW)-1:
                    mr = self.cells[y][x+1]
                
                if y < int(HEIGHT/CH) - 1:
                    if x > 0:
                        ll = self.cells[y+1][x-1]
                    if x < (WIDTH/CW)-1:
                        lr = self.cells[y+1][x+1]
                    lm = self.cells[y+1][x]
                
                n_neighbours = ul + um + ur + ml + mr + ll + lm + lr

                if self.cells[y][x] == 1 and 2 <= n_neighbours <= 3:
                    self.cells[y][x] = 1
                elif self.cells[y][x] == 0 and n_neighbours == 3:
                    self.cells[y][x] = 1
                else:
                    self.cells[y][x] = 0


    def __render(self):
        for y in range(int(HEIGHT/CH)):
            for x in range(int(WIDTH/CW)):
                rect = pygame.Rect(x*CW,y*CH,CW,CH)
                if self.cells[y][x] == 0:
                    colour = BLACK
                else:
                    colour = WHITE
                pygame.draw.rect(self.surface, colour, rect)


    def __init_cells(self):
        rand = random.Random()
        rand.seed(datetime.now().microsecond)
        self.cells = list()
        for y in range(int(HEIGHT/CH)):
            self.cells.append(list())
            for x in range(int(WIDTH/CW)):
                state = rand.randint(0, 1)
                self.cells[y].append(state)
        

if __name__ == '__main__':
    game = Game()
    game.init_game()
    game.run()