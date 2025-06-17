# main game grid

import pygame
from settings import *

class Board:
    def __init__(self):
        self.grid = [[COLOURS["background"] for count in range(GRID_COLS)] for count in range(GRID_ROWS)] # creates grid of black

    def isvalidposition(self, piece): # check if the piece is in a valid position.
        for row, col in piece.get_block_positions(): # parses the row/column from the block positions.
            if not (0 <= col < GRID_COLS and 0 <= row < GRID_ROWS):
                return False # out of bounds.
            
            if self.grid[row][col] != COLOURS["background"]:
                return False # collision with another piece
            
        return True
        
    def lockpiece(self, piece): # locks piece in place on the grid
        for row, col in piece.get_block_positions():
            self.grid[row][col] = piece.colour

    def clear_lines(self):
        lines_cleared = 0
        new_grid = [row for row in self.grid if any(cell == COLOURS['background'] for cell in row)] # chekcs if at least one cell is background cell
        # only not full rows are kept in new_grid

        lines_cleared = GRID_ROWS - len(new_grid)

        for count in range(lines_cleared):
            new_grid.insert(0, [COLOURS['background'] for count in range(GRID_COLS)])

        self.grid = new_grid
        return lines_cleared
        
    def draw(self, screen):
        for r_idx, row in enumerate(self.grid):
            for c_idx, colour in enumerate(row):
                # draw filled block
                pygame.draw.rect(screen, colour, # in (screen, colour, X, Y, width, height)
                                 (GAME_AREA_X + c_idx * BLOCK_SIZE,
                                 GAME_AREA_Y + r_idx * BLOCK_SIZE,
                                 BLOCK_SIZE, BLOCK_SIZE))
                
                # drawing the gridlines:
                for x in range(GAME_AREA_X, GAME_AREA_X + GAME_AREA_WIDTH + 1, BLOCK_SIZE):
                    pygame.draw.line(screen, COLOURS['grid'],
                                     (x, GAME_AREA_Y),
                                     (x, GAME_AREA_Y + GAME_AREA_HEIGHT))
                for y in range(GAME_AREA_Y, GAME_AREA_HEIGHT + 1, BLOCK_SIZE):
                    pygame.draw.line(screen, COLOURS['grid'],
                                     (GAME_AREA_X, y),
                                     (GAME_AREA_X + GAME_AREA_WIDTH, y))


