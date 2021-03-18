import random

import pygame
from datetime import datetime

from constants import *

class Game(object):

    def __init__(self):
        super().__init__()
        self.surface: pygame.Surface = None
        self.__running = False
        self.__sim_running = False
        self.cells = [] # 0=dead, 1=alive

    def init_game(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Conways Game of Life')
        self.__init_cells()
        self.__running = True


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
                self.__input(event)

            
            while lag >= MS_PER_UPDATE:
                if self.__sim_running:
                    self.__update()
                lag -= MS_PER_UPDATE
            self.__render()
            pygame.display.flip()

            last_time = current_time


    def __input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.__sim_running = not self.__sim_running
            
            if not self.__sim_running:
                if event.key == pygame.K_s:
                    self.__save_cell_state_to_disk()
                if event.key == pygame.K_l:
                    self.__load_cell_state_from_disk()
                if event.key == pygame.K_r:
                    self.__init_cells()
            
        if not self.__sim_running:
            if pygame.mouse.get_pressed():
                pos = pygame.mouse.get_pos()
                # calc rect that was pressed
                ry = pos[1] % CH
                rx = pos[0] % CW
                y = (pos[1] - ry) 
                x = (pos[0] - rx) 
                if 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
                    ix = int(x/CW)
                    iy = int(y/CH)
                    state = self.cells[iy][ix]
                    if pygame.mouse.get_pressed()[0]: # left click
                        self.cells[iy][ix] = 1
                    elif pygame.mouse.get_pressed()[2]: # right click
                        self.cells[iy][ix] = 0


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
        # rand = random.Random()
        # rand.seed(datetime.now().microsecond)
        self.cells = list()
        for y in range(int(HEIGHT/CH)):
            self.cells.append(list())
            for x in range(int(WIDTH/CW)):
                # state = rand.randint(0, 1)
                state = 0
                self.cells[y].append(state)


    def __save_cell_state_to_disk(self):
        s = f'{WIDTH} {HEIGHT}\n'
        name = str(input("enter name of save: "))
        for row in self.cells:
            for col in row:
                s += str(col)+' '
            s += '\n'
        try:
            with open(f'{name}.txt', 'w') as f:
                f.write(s)
                f.close()
            return True
        except:
            return False
    

    def __load_cell_state_from_disk(self):
        self.cells = list()
        name = str(input("name of save: "))
        with open(f'{name}.txt', 'r') as f:
            l1 = f.readline().strip('\n').split(' ')
            WIDTH = int(l1[0])
            HEIGHT = int(l1[1])
            for line in f.readlines():
                line = line.strip('\n').split(' ')[:-1]
                self.cells.append([int(c) for c in line])


if __name__ == '__main__':
    game = Game()
    game.init_game()
    game.run()