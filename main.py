import random
import time
import os
import pygame

pixel_size = 10

class Board():
    def __init__(self, width : int = 84, height : int = 42):
        self.width=width
        self.height=height

        self.board = []
        for y in range(0, 42):
            x_list = []
            for x in range(0, 84):
                x_list.append(0)
            self.board.append(x_list)
          
    def add_glider(self) -> None:
        self.board[9][12] = 1
        self.board[9][13] = 1
        self.board[9][14] = 1
        self.board[8][14] = 1
        self.board[7][13] = 1

    def check_neighbors(self, pos) -> int:
        count = 0
        #  check that we are in range       # check value of board at this valid range
        if pos['x'] - 1 >= 0 \
                and self.board[pos['y']][pos['x']-1] == 1:
            count += 1 # left

        if pos['x'] + 1 < self.width \
                and self.board[pos['y']][pos['x']+1] == 1: 
            count += 1 # right

        if pos['y'] - 1 >= 0 \
                and self.board[pos['y']-1][pos['x']] == 1:
            count += 1 # down

        if pos['y'] + 1 < self.height \
                and self.board[pos['y']+1][pos['x']] == 1:
            count += 1 # up

        if pos['y'] - 1 >= 0 \
                and pos['x'] - 1 >=  0 \
                and self.board[pos['y']-1][pos['x']-1] == 1:
            count += 1 # up

        if pos['y'] + 1 < self.height \
                and pos['x'] + 1 < self.width \
                and self.board[pos['y'] + 1][pos['x'] + 1] == 1:
            count += 1 # up

        if pos['y'] - 1 >= 0 \
                and pos['x'] + 1 < 84 \
                and self.board[pos['y']-1][pos['x']+1] == 1: 
            count += 1 # up

        if pos['y'] + 1 < self.height \
                and pos['x'] - 1 >= 0 \
                and self.board[pos['y']+1][pos['x']-1] == 1:
            count += 1 # up


        # return updated cell
        alive = self.board[pos['y']][pos['x']] == 1
        if alive and count == 2:
            return 1
        elif alive and count == 3:
            return 1
        elif not alive and count == 3:
            return 1
        else:
            return 0

    def check_all_neighbors(self) -> None:
        board=[]
        for y in range(0, 42):
            x_board=[]
            for x in range(0, 84):
                pos= {'x':x,'y':y}
                x_board.append(self.check_neighbors(pos))
            board.append(x_board)
        self.board = board    

    def show_board(self, screen) -> None:
        _y=0
        for y in range(0, 42* pixel_size, pixel_size):
            _x=0
            for x in range(0, 84 * pixel_size, pixel_size):
                color = (255, 0, 0)
                if self.board[_y][_x] == 1:
                    color = (255, 255, 255)
                pygame.draw.rect(screen, color, (x, y, pixel_size, pixel_size))
                _x+=1
            _y+=1

board = Board(84, 42)
board.add_glider()

screen = pygame.display.set_mode((84 * pixel_size, 42 * pixel_size))
board.show_board(screen)
pygame.display.flip()

loop=1
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop=0
        if event.type == pygame.KEYDOWN:
            if event.key == 27:
                loop=0
            if event.unicode == 'a':
                board.add_glider()

    time.sleep(0.1)

    color = (0, 0, 0)
    position = (0, 0, 42 * pixel_size, 42 * pixel_size)
    pygame.draw.rect(screen, color, position)
    board.check_all_neighbors()
    board.show_board(screen)
    pygame.display.flip()

