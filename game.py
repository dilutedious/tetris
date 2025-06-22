# core game engine

import pygame
import random
from settings import *
from piece import Piece
from board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.fall_delay = FALL_DELAY
        self.fall_time = 0

        self.piece_bag = list(SHAPES.keys())
        random.shuffle(self.piece_bag)

        self.current_piece = self._get_new_piece()
        self.next_pieces = [self._get_new_piece() for count in range(3)]

    def _get_new_piece(self):
        if not self.piece_bag: # if the bag is empty, refill with all shape names from shapes and shuffle.
            self.piece_bag = list(SHAPES.keys())
            random.shuffle(self.piece_bag)
        shape_name = self.piece_bag.pop()
        return Piece(shape_name)
    
    def _update_piece(self):
        self.current_piece = self.next_pieces.pop(0)
        self.next_pieces.append(self._get_new_piece()) # gets from the bag and displays as next piece
        if not self.board.isvalidposition(self.current_piece):
            self.game_over = True
    
    def _check_levelup(self):
        if self.lines >= self.level * LINES_PERLEVEL:
            self.level += 1
            self.fall_delay = max(100, int(FALL_DELAY * (DELAY_REDUCTION ** (self.level - 1))))
    
    def update(self, dt):
        if self.game_over:
            return
        self.fall_time += dt
        if self.fall_time >= self.fall_delay:
            self.fall_time = 0
            self.move_piece(0, 1)
        
    def move_piece(self, dx, dy):
        if self.game_over: return
        self.current_piece.move(dx, dy)
        if not self.board.isvalidposition(self.current_piece):
            self.current_piece.move(-dx, -dy) #reverts the mvoe
            if dy > 0: # if downwards move, then it landed.
                self.board.lockpiece(self.current_piece)
                self.score += 11
                cleared_lines = self.board.clear_lines()
                if cleared_lines > 0:
                    CLEARLINE_SOUND.play()
                    self.score += SCORES.get(cleared_lines, 0) # if not in the dictionary, returns 0
                    self.lines += cleared_lines
                    self._check_levelup()
                self._update_piece()

    def rotate_piece(self):
        if self.game_over: return

        original_rotation = self.current_piece.rotation
        self.current_piece.rotate()

        if self.board.isvalidposition(self.current_piece):
            ROTATE_SOUND.play()
            return # simple rotation is valid
        
        # wall kicking
        offsets = [-1, 1, -2, 2] # tries moving left/right
        for offset in offsets:
            self.current_piece.move(offset, 0)
            if self.board.isvalidposition(self.current_piece):
                ROTATE_SOUND.play()
                return # if it found a valid position
            self.current_piece.move(-offset, 0) # reverts changes

        # if all wall kicks fail, rever tthe rotation instead.
        self.current_piece.rotation = original_rotation
        self.current_piece.shape = self.current_piece.shape_data['rotations'][self.current_piece.rotation]

    def hard_drop(self):
        if self.game_over: return

        while self.board.isvalidposition(self.current_piece):
            self.current_piece.move(0,1)
        self.current_piece.move(0,-1) # moves back one step to be in a valid spot.
        self.board.lockpiece(self.current_piece)
        self.score += 11
        cleared_lines = self.board.clear_lines()
        if cleared_lines > 0:
            CLEARLINE_SOUND.play()
            self.score += SCORES.get(cleared_lines, 0)
            self.lines += cleared_lines
            self._check_levelup()
        self._update_piece()

    def draw(self, screen):
        self.board.draw(screen)
        # draw current piece.
        if not self.game_over:
            piece_colour = self.current_piece.colour
            for row, col, in self.current_piece.get_block_positions():
                pygame.draw.rect(screen, piece_colour,
                                 (GAME_AREA_X + col * BLOCK_SIZE,
                                  GAME_AREA_Y + row * BLOCK_SIZE,
                                  BLOCK_SIZE - 1, BLOCK_SIZE -1))
            