# settings.py (all the constants are in capitals)

import pygame

# screen and layout
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 850
PADDING = 50

GAME_AREA_WIDTH = 500
GAME_AREA_HEIGHT = 750
GAME_AREA_X = PADDING
GAME_AREA_Y = PADDING

# grid dimensions
GRID_COLS = 10
GIRD_ROWS = 15
BLOCK_SIZE = GAME_AREA_WIDTH // GRID_COLS # floor division → should be 50.

# side panel dimensions
SIDE_PANEL_WIDTH = 250
SIDE_PANEL_HEIGHT = SCREEN_HEIGHT - (2 * PADDING) # should be 750
SIDE_PANEL_X = GAME_AREA_X + GAME_AREA_WIDTH + PADDING

# next piece area
UPCOMING_AREA_HEIGHT = 600
UPCOMING_AREA_Y = PADDING

# score area
SCORE_AREA_HEIGHT = 100
SCORE_AREA_Y = SCREEN_HEIGHT - PADDING - SCORE_AREA_HEIGHT

# colours dictionary
COLOURS = {
    'background': '#1c1c1c',
    'grid': '#3c3c3c',
    'text': '#ffffff',
    'white': '#ffffff',
    'black': '#000000',
    # block colours
    'red': '#ff0c72',
    'orange': '#ff8e0e',
    'yellow': '#ffe138',
    'green': '#0fff73',
    'lblue': '#10c2ff', # light blue for the squares
    'dblue': '#3777ff', # dark blue for the s shape
    'magenta': '#f538ff' 
}

SHAPES = { # sliced shapes into rows (top, middle, bottom)
    'T': {'colour': 'red', 'rotations': [
        [[0,0,0], [0,1,0], [1,1,1]]
        [[1,0,0], [1,1,0], [1,0,0]]
        [[1,1,1], [0,1,0], [0,0,0]]
        [[0,0,1], [0,1,1], [0,0,1]]
    ]},
    'L': {'colour': 'magenta', 'rotations': [
        [[0,1,0], [0,1,0], [0,1,1]]
        [[0,0,0], [1,1,1], [1,0,0]]
        [[1,1,0], [0,1,0], [0,1,0]]
        [[0,0,1], [1,1,1], [0,0,0]]
    ]},
    'J': {'colour': 'orange', 'rotations': [
        [[0,1,0], [0,1,0], [1,1,0]]
        [[1,0,0], [1,1,1], [0,0,0]]
        [[0,1,1], [0,1,0], [0,1,0]]
        [[0,0,0], [1,1,1], [0,0,1]]
    ]},
    'S': {'colour': 'dblue', 'rotations': [
        [[0,0,0], [0,1,1], [1,1,0]]
        [[1,0,0], [1,1,0], [0,1,0]]
        [[0,1,1], [1,1,0], [0,0,0]]
        [[0,1,0], [0,1,1], [0,0,1]]
    ]},
    'Z': {'colour': 'yellow', 'rotations': [
        [[0,0,0], [1,1,0], [0,1,1]]
        [[0,1,0], [1,1,0], [1,0,0]]
        [[1,1,0], [0,1,1], [0,0,0]]
        [[0,0,1], [0,1,1], [0,1,0]]
    ]},
    'I': {'colour': 'green', 'rotations': [
        [[0,0,1,0], [0,0,1,0], [0,0,1,0], [0,0,1,0]]
        [[0,0,0,0], [0,0,0,0], [1,1,1,1], [0,0,0,0]]
        [[0,1,0,0], [0,1,0,0], [0,1,0,0], [0,1,0,0]]
        [[1,1,1,1], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    ]},
    'O': {'colour': 'lblue', 'rotations': [
        [[0,1,1], [0,1,1], [0,1,1]]
        [[0,1,1], [0,1,1], [0,1,1]]
        [[0,1,1], [0,1,1], [0,1,1]]
        [[0,1,1], [0,1,1], [0,1,1]]
    ]},
}

# game mechanics

FALL_DELAY = 375 # milliseconds
DELAY_REDUCTION = 0.85 # percentage of original (will decrease to this level)



