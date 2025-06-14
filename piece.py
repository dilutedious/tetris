# tetris piece class

import pygame
from settings import *

class Piece:
    def __init__(self, shape_name):
        self.shape_name = shape_name
        self.shape_data = SHAPES[shape_name]
        self.colour = COLOURS[self.shape_data['colour']]
        self.rotation = 0
        self.shape = self.shape_data['rotations'][self.rotation]

        # position

        self.x = GRID_COLS // 2 - len(self.shape[0]) // 2 # places the block in the middle of the screen. (half grid minus half block size)
        self.y = 0 # 0 is at the top.

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape_data['rotations'])
        self.shape = self.shape_data['rotations'][self.rotation]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_block_positions(self): # returns GRID coordinates for each piece of block
        positions = []
        for r_idx, row in enumerate(self.shape):
            for c_idx, cell in enumerate(row):
                if cell:
                    positions.append((self.y + r_idx, self.x + c_idx))
        return positions
    
    

