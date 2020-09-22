import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

CELL = 100
SEMI_CELL = int (CELL / 2)
RADIUS = int (SEMI_CELL / 1.15)
HOLE_RADIUS = int (SEMI_CELL / 1.2)

NUMBER_COLUMNS = 7
NUMBER_ROWS = 6

SCREEN_WIDTH = CELL * NUMBER_COLUMNS
SCREEN_HEIGHT = CELL * (NUMBER_ROWS + 1)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

board = np.zeros ((NUMBER_COLUMNS, NUMBER_ROWS))
player = True
game_over = False
winner = -1

pygame.init()
myfont = pygame.font.SysFont("monospace", int(CELL/100*75))

def display_front_board():
    front_board = pygame.Surface ((SCREEN_WIDTH, SCREEN_HEIGHT-CELL), pygame.SRCALPHA)
    front_board.fill (BLUE)

    hole = pygame.Surface ((CELL, CELL), pygame.SRCALPHA)
    pygame.draw.circle (hole, (BLACK), (SEMI_CELL, SEMI_CELL), HOLE_RADIUS)

    for x in range (0, SCREEN_WIDTH, CELL):
        for y in range (0, SCREEN_WIDTH, CELL):
            front_board.blit (hole, (x,y), special_flags=pygame.BLEND_RGBA_SUB )

    screen.blit (front_board, (0, CELL))

def display_disk_on_top (x):
    y = SEMI_CELL
    display_disk (x,y)

def display_disk (x,y):
    pygame.draw.circle (screen, get_player_color(), (x,y), RADIUS)  

def drop_disk(x, limit_y):
    limit_y = SCREEN_HEIGHT - (CELL * (limit_y + 1))
    limit_y = int (limit_y - SEMI_CELL)
    acel = 10
    vel = acel
    y = vel + SEMI_CELL
    while y < limit_y:
        y += vel
        vel += acel
        screen.fill (BLACK)
        display_disks_in_board()
        display_disk (x,y)
        display_front_board()
        pygame.display.update()
        pygame.time.delay(50)

def get_player_color():
    if player:
        return RED
    else:
        return YELLOW

def get_disk_color (one_or_two):
    if one_or_two == 1:
        return RED
    else:
        return YELLOW

def player_int():
    if player:
        return 1
    else:
        return 2

def display_disks_in_board():
    for x in range (NUMBER_COLUMNS):
        for y in range (NUMBER_ROWS):
            flip_board = np.flip(board, 1)
            color = flip_board[x][y]
            if color != 0:
                color = get_disk_color(color)
                screen_x = x * CELL + SEMI_CELL
                screen_y = (y+1) * CELL +  SEMI_CELL
                pygame.draw.circle (screen, color, (screen_x,screen_y), RADIUS)

def get_last_disk(x):
    for y in range (NUMBER_ROWS):
        if board[x][y] == 0:
            return y
    return -1
        
def check_winner():
    for x in range (NUMBER_COLUMNS-3):
        for y in range (NUMBER_ROWS):
            ref = board[x][y]
            if ref != 0 and board[x+1][y] == ref and board[x+2][y] == ref and board[x+3][y] == ref:
                return ref
    for x in range (NUMBER_COLUMNS):
        for y in range (NUMBER_ROWS-3):
            ref = board[x][y]
            if ref != 0 and board[x][y+1] == ref and board[x][y+2] == ref and board[x][y+3] == ref:
                return ref
    for x in range (NUMBER_COLUMNS-3):
        for y in range (NUMBER_ROWS-3):
            ref = board[x][y]
            if ref != 0 and board[x+1][y+1] == ref and board[x+2][y+2] == ref and board[x+3][y+3] == ref:
                return ref
    for x in range (3, NUMBER_COLUMNS):
        for y in range (NUMBER_ROWS-3):
            ref = board[x][y]
            if ref != 0 and board[x-1][y+1] == ref and board[x-2][y+2] == ref and board[x-3][y+3] == ref:
                return ref
    if 0 not in board: # TIE
        return 0
    else: # NO WINNER
        return -1
    
def display_winner(item):
    pygame.draw.rect (screen, BLACK, (0,0,SCREEN_WIDTH, CELL))
    x = (CELL/100)*20
    y = (CELL/100)*10
    if item == 1:
        label = myfont.render("Player 1 wins!!", 1, RED)
    elif item ==2:
        label = myfont.render("Player 2 wins!!", 1, YELLOW)
    elif item == 0:
        label = myfont.render("T I E", 1, YELLOW)
        x = CELL/100*240

    screen.blit(label, (x,y))
    pygame.display.update()

                

while not game_over:
    if winner >= 0:
        game_over = True

    screen.fill (BLACK)

    mouse_x = pygame.mouse.get_pos()[0]
    mouse_x = mouse_x - (mouse_x % CELL) + SEMI_CELL
    display_disk_on_top (mouse_x)

    display_disks_in_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            board_x = int (mouse_x / CELL)
            board_y = get_last_disk(board_x)
            if board_y != -1:
                drop_disk (mouse_x, board_y)
                board[board_x][board_y] = player_int()
                flip_board = np.rot90(board)
                winner = check_winner()
                player = not player

    display_front_board()
    pygame.display.update()
    

# OUTSIDE GAME_OVER LOOP
display_winner (winner)
pygame.time.delay(3000)
pygame.quit()
