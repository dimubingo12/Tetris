# utils.py

import pygame

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

def draw_grid(surface, grid):
    surface.fill((0,0,0))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (j*20, i*20, 20, 20), 0)

    # Draw gridlines
    for i in range(len(grid)):
        pygame.draw.line(surface, GRAY, (0, i*20), (200, i*20))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, GRAY, (j*20, 0), (j*20, 400))

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 20)
    label = font.render('Next Shape:', 1, (255,255,255))

    sx = 220
    sy = 50
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*20, sy + i*20, 20, 20), 0)

    surface.blit(label, (sx + 10, sy - 30))

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
