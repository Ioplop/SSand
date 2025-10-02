import numpy as np
import pygame

SAND = 1
WALL = -1
EMPTY = 0

width = 160
height = 90
falling_side = 1

sand_map = np.zeros((height, width), dtype=int)
moved_map = np.full((height, width), False, dtype=bool)
vupdate_map = np.full((height, width), True, dtype=bool)

def take_one_vertical(x: int, y: int):
    while y >= 0 and sand_map[y, x] == SAND and not moved_map[y, x]:
        moved_map[y, x] = True
        y -= 1
    moved_map[y + 1, x] = False
    vupdate_map[y + 1, x] = True
    sand_map[y + 1, x] = EMPTY
        
def fall_from_to(from_x: int, from_y: int, to_x: int, to_y: int):
    take_one_vertical(from_x, from_y)
    vupdate_map[to_y, to_x] = True
    moved_map[to_y, to_x] = True
    sand_map[to_y, to_x] = SAND

def vertical_fall():
    for y in range(1, height):
        for x in range(width):
            if sand_map[y, x] == EMPTY and sand_map[y-1, x] == SAND and not moved_map[y-1, x]:
                fall_from_to(x, y-1, x, y)
                
def horizontal_fall():
    from_x = 0 if falling_side == 1 else 1
    to_x = width - 1 if falling_side == 1 else width
    for y in range(1, height):
        for x in range(from_x, to_x):
            if sand_map[y, x] == EMPTY and sand_map[y-1, x + falling_side] == SAND and not moved_map[y-1, x + falling_side]:
                fall_from_to(x + falling_side, y-1, x, y)

def both_horizontal():
    global falling_side
    horizontal_fall()
    falling_side *= -1
    horizontal_fall()
    
def full_fall():
    vertical_fall()
    both_horizontal()
