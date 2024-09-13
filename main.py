# main.py

import pygame
import sys
import random
from shapes import Shape
from utils import draw_grid, create_grid, check_lost, draw_next_shape, clear_rows

# Initialize Pygame
pygame.init()

# Global Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = Shape(5, 0)
    next_piece = Shape(5, 0)
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27

        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # Increase difficulty over time
        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        # Piece falls automatically
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (current_piece.valid_space(grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not current_piece.valid_space(grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not current_piece.valid_space(grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not current_piece.valid_space(grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not current_piece.valid_space(grid):
                        current_piece.rotation -= 1

        shape_pos = current_piece.convert_shape_format()

        # Add piece to the grid
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # When piece lands
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = Shape(5, 0)
            change_piece = False
            # Clear rows and update score
            cleared_rows = clear_rows(grid, locked_positions)
            score += cleared_rows * 10

        draw_grid(screen, grid)
        draw_next_shape(next_piece, screen)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

    pygame.display.quit()
    sys.exit()

if __name__ == '__main__':
    main()
