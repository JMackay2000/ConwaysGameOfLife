import sys
from datetime import datetime

import pygame

BLACK = (0,0,0,1)
WHITE = (255,255,255,1)

class Game(object):

    def __init__(self):
        super().__init__()
        self.surface: pygame.Surface = None
        self.__running = False
        self.__sim_running = False
        self.cells = [] # 0 is dead, 1 is alive
        self.width = 800
        self.height = 800
        self.cellw = 10
        self.cellh = 10


    def init_game(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
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
                    self.__quit()
                    return
                elif event.type == pygame.VIDEORESIZE:
                    self.__resize(event.w, event.h)
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
                elif event.key == pygame.K_l:
                    self.__load_cell_state_from_disk()
                elif event.key == pygame.K_r:
                    self.__init_cells()
                elif event.key == pygame.K_q:
                    self.__quit()
        
        # draw cells with mouse if simulation isn't running
        if not self.__sim_running and pygame.mouse.get_pressed():
            pos = pygame.mouse.get_pos()
            # calc rect that was pressed
            ry = pos[1] % self.cellh
            rx = pos[0] % self.cellw
            y = (pos[1] - ry) 
            x = (pos[0] - rx) 
            if 0 <= x <= self.width and 0 <= y <= self.height:
                ix = int(x/self.cellw)
                iy = int(y/self.cellh)
                if pygame.mouse.get_pressed()[0]: # left click
                    self.cells[iy][ix] = 1
                elif pygame.mouse.get_pressed()[2]: # right click
                    self.cells[iy][ix] = 0


    def __update(self):
        for y in range(int(self.height/self.cellh)):
            for x in range(int(self.width/self.cellw)):
                ul = um = ur = ml = mr = ll = \
                    lm = lr = 0
                if y > 0:
                    if x > 0:
                        ul = self.cells[y-1][x-1]
                    um = self.cells[y-1][x]
                    if x < (self.width/self.cellw)-1:
                        ur = self.cells[y-1][x+1]

                if x > 0:
                    ml = self.cells[y][x-1]
                if x < (self.width/self.cellw)-1:
                    mr = self.cells[y][x+1]
                
                if y < int(self.height/self.cellh) - 1:
                    if x > 0:
                        ll = self.cells[y+1][x-1]
                    if x < (self.width/self.cellw)-1:
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
        for y in range(int(self.height/self.cellh)):
            for x in range(int(self.width/self.cellw)):
                rect = pygame.Rect(x*self.cellw,y*self.cellh,self.cellw,self.cellh)
                if self.cells[y][x] == 0:
                    colour = BLACK
                else:
                    colour = WHITE
                pygame.draw.rect(self.surface, colour, rect)


    def __init_cells(self):
        self.cells = list()
        for y in range(int(self.height/self.cellh)):
            self.cells.append(list())
            for x in range(int(self.width/self.cellw)):
                state = 0
                self.cells[y].append(state)


    def __save_cell_state_to_disk(self):
        s = f'{self.width} {self.height}\n'
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
        except IOError:
            return False
    

    def __load_cell_state_from_disk(self):
        self.cells = list()
        name = str(input("name of save: "))
        with open(f'{name}.txt', 'r') as f:
            l1 = f.readline().strip('\n').split(' ')
            self.width = int(l1[0])
            self.height = int(l1[1])
            for line in f.readlines():
                line = line.strip('\n').split(' ')[:-1]
                self.cells.append([int(c) for c in line])


    def __resize(self, new_width: int, new_height: int):
        sfh = new_height / self.height
        sfw = new_width / self.width
        self.width *= sfw
        self.height *= sfh
        self.cellw *= sfw
        self.cellh *= sfh
        self.surface = pygame.display.set_mode((int(self.width), int(self.height)), pygame.RESIZABLE)


    def __quit(self):
        self.__running = False
        pygame.quit()
        sys.exit(0)


if __name__ == '__main__':
    game = Game()
    game.init_game()
    game.run()