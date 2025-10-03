import numpy as np
import pygame
from random import random
pygame.init()


# Constants
SAND = 1
WALL = -1
EMPTY = 0

color_mapping = {
    SAND: (200, 200, 50),
    WALL: (255, 255, 255),
    EMPTY: (0, 0, 0)
}

# World dimensions
width = 200
height = 150

# Status
falling_side = 1
debug_helper = 0

# Sand matrices
sand_map = np.zeros((height, width), dtype=int)
moved_map = np.full((height, width), False, dtype=bool)
# Flags
paint_pixels = []

# pygame display
screen = pygame.display.set_mode((width, height))

def debug_help():
    global debug_helper
    print(f"DEBUG: {debug_helper}")
    debug_helper += 1

def take_one_vertical(x: int, y: int):
    while y >= 0 and sand_map[y, x] == SAND and not moved_map[y, x]:
        moved_map[y, x] = True
        y -= 1
    moved_map[y + 1, x] = False
    paint_pixels.append((y+1, x))
    sand_map[y + 1, x] = EMPTY
        
def fall_from_to(from_x: int, from_y: int, to_x: int, to_y: int):
    take_one_vertical(from_x, from_y)
    paint_pixels.append((to_y, to_x))
    moved_map[to_y, to_x] = True
    sand_map[to_y, to_x] = SAND
    
def fast_fall_from_to(from_x: int, from_y: int, to_x: int, to_y: int):
    paint_pixels.append((from_y, from_x))
    moved_map[from_y, from_x] = False
    sand_map[from_y, from_x] = EMPTY
    
    paint_pixels.append((to_y, to_x))
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
    for y in range(height-1, 0, -1):
        for x in range(from_x, to_x):
            if sand_map[y, x] == EMPTY and sand_map[y-1, x + falling_side] == SAND and not moved_map[y-1, x + falling_side]:
                fast_fall_from_to(x + falling_side, y-1, x, y)

def both_horizontal():
    global falling_side
    horizontal_fall()
    falling_side *= -1
    horizontal_fall()
    
def clear_flags():
    global moved_map
    moved_map = np.full((height, width), False, dtype=bool)
    paint_pixels.clear()

def full_fall():
    clear_flags()
    vertical_fall()
    both_horizontal()

def paint_screen():
    for y in range(height):
        for x in range(width):
            screen.set_at((x, y), color_mapping[sand_map[y, x]])

def update_screen():
    for y, x in paint_pixels:
        screen.set_at((x, y), color_mapping[sand_map[y, x]])
    pygame.display.flip()

def reset_sand():
    global sand_map
    sand_map = np.zeros((height, width), dtype=int)
    # Draw sandmap walls
    for y in range(height):
        sand_map[y, 0] = WALL
        sand_map[y, width - 1] = WALL
    for x in range(width):
        sand_map[height-1, x] = WALL
    
    """
    # Draw random sand
    for x in range(1, width-1):
        for y in range(0, height-1):
            if random() <= 0.3:
                sand_map[y, x] = SAND
    """
    for y in range(height//2):
        for x in range(int(width/2.5), width - int(width/2.5)):
            sand_map[y, x] = SAND
    
    # Draw the window
    paint_screen()
    
reset_sand()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_sand()
    full_fall()
    update_screen()
