import numpy as np
import pygame
import random

class GameOfLife:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.board = np.zeros([row,col])

    def change_cell(self, row, col):
        if self.board[row][col] == 0:
            self.board[row][col] = 1
        else:
            self.board[row][col] = 0

    def count_alive(self, row, col):
        add = []
        for i in [-1, 1,0]:
            for j in [-1, 1,0]:
                add.append([i,j])
        count = 0
        for i in add:
            c = col + i[0]
            r = row + i[1]
            if c<0 or r<0 or c>=len(self.board[0]) or r>=len(self.board) or c==col and r==row:
                continue
            if self.board[r][c] == 1:
                count+=1
        return count
    
    def randomize(self, a, b):
        for _ in range(random.randint(a,b)):
            self.change_cell(random.randint(0,self.row-1), random.randint(0,self.col-1))

    def step(self):
        change = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):

                if self.board[row][col] == 0:
                    if self.count_alive(row, col) == 3:
                        change.append([row, col])
                
                if self.board[row][col] == 1:
                    if self.count_alive(row, col) not in [2,3]:
                        change.append([row, col])
        
        for i in change:
            self.change_cell(i[0], i[1])

    def draw(self, size, rand_a=10, rand_b=100,color=(0, 255, 0), bgcolor=(0,0,0), frames=10):
        pygame.init()
        screen = pygame.display.set_mode(size)
        running = True
        create = True
        clock = pygame.time.Clock()
        while running:
            screen.fill(bgcolor)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if create:
                            create=False
                            print("Create")
                        else:
                            create=True
                            print("Simulating")
                    if event.key == pygame.K_r:
                        self.randomize(rand_a, rand_b)

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.change_cell(int(pos[0]/size[0]*self.row), int(pos[1]/size[1]*self.col))
            for i in range(self.row):
                for j in range(self.col):
                    if self.board[i][j]==1:
                        pygame.draw.rect(screen, color,((size[0]/self.row*i), int(size[0]/self.row*j), (size[0]/self.row),int(size[0]/self.row)))
            
            pygame.display.update()
    
            if not create:
                self.step()        
                clock.tick(frames)

test = GameOfLife(100,100)
test.draw((1000,1000))
