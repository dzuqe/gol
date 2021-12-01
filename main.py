import random
import time
import os
import pygame
from typing import List, Dict

pixel_size = 12
screen_width = 50
screen_height = 50

class Reader:
    def __init__(self):
        pass

    def read(self, fname) -> List[List[int]]:
        lines = open(fname, 'r').readlines()
        y_list = []
        for line in lines:
            y_list.append([0 if x == '.' else 1 for x in line[:-1]])
        return y_list

    def get_board(self) -> List[List[int]]:
        return self.board

class Board():
    def __init__(self, width : int, height : int):
        self.width=width
        self.height=height
        self.reader = Reader()
        self.palette = [
            (0,     0xff, 0xff),
            (0,     0x80, 0xff),
            (0,     0xff, 0x80)
        ]

        self.board = []
        for y in range(0, screen_height):
            x_list = []
            for x in range(0, screen_width):
                x_list.append(0)
            self.board.append(x_list)
          
    def add_object(self, name, offx, offy):
        object = self.reader.read(f"./objects/{name}.txt")
        offset_x = offx
        offset_y = offy
        y = 0
        for py in range(offset_y, offset_y + len(object)):
            x = 0
            for px in range(offset_x, offset_x + len(object[0])):
                self.board[py][px] = object[y][x]
                x += 1
            y += 1    

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
                and pos['x'] + 1 < screen_width \
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
        for y in range(0, screen_height):
            x_board=[]
            for x in range(0, screen_width):
                pos= {'x':x,'y':y}
                x_board.append(self.check_neighbors(pos))
            board.append(x_board)
        self.board = board    

    def show_board(self, screen) -> None:
        _y=0
        for y in range(0, screen_height* pixel_size, pixel_size):
            _x=0
            for x in range(0, screen_width * pixel_size, pixel_size):
                color = (0xfc, 0xfc, 0x6c)
                if self.board[_y][_x] == 1:
                    color = self.palette[random.randrange(0, len(self.palette))]
                pygame.draw.rect(screen, color, (x, y, pixel_size, pixel_size))
                _x+=1
            _y+=1

board = Board(screen_width, screen_height)
#board.add_object('glider_duplicator', 0, 0)
board.add_object('backrake', screen_width - 30, screen_height - 20)

pygame.init()
screen = pygame.display.set_mode((screen_width * pixel_size, screen_height * pixel_size))

font = pygame.font.SysFont('impact', 60)
text_color = (0x4a, 0xa0, 0x03)
text1 = font.render("scarred", True, text_color)
text2 = font.render("games", True, text_color)

background = pygame.image.load('./objects/plant.png').convert_alpha()

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
    position = (0, 0, screen_height * pixel_size, screen_height * pixel_size)
    pygame.draw.rect(screen, color, position)
    board.check_all_neighbors()
    board.show_board(screen)

    screen.blit(background, (0,0))

    screen.blit(text1, (20,20))
    screen.blit(text2, (20,80))

    pygame.display.flip()

