# handles all of the UI drawing.

import pygame
from settings import *

class UI:
    def __init__(self):
        # loading fonts:
        try:
            self.title_font = pygame.font.Font(FONT_PATH, 64)
            self.score_font = pygame.font.Font(FONT_PATH, 32)
            self.menu_font = pygame.font.Font(FONT_PATH, 48)
            self.input_font = pygame.font.Font(FONT_PATH, 40)
        except FileNotFoundError:
            print(f"Font file not found at {FONT_PATH}. Using default font.")
            self.title_font = pygame.font.Font(None, 64)
            self.score_font = pygame.font.Font(None, 32)
            self.menu_font = pygame.font.Font(None, 48)
            self.input_font = pygame.font.Font(None, 40)
        
        # loading images
        try:
            self.title_image = pygame.image.load(TITLE_IMG).convert_alpha()
            self.gameover_image = pygame.image.load(GAMEOVER_IMG).convert_alpha()
            self.playbutton_images = {
                'normal': pygame.image.load(PLAY_BTN_IMG).convert_alpha(),
                'hover': pygame.image.load(PLAY_BTNHVR_IMG).convert_alpha(),
                'click': pygame.image.load(PLAY_BTNCLK_IMG).convert_alpha()
            }
        except pygame.error as e:
            print(f"Error loading images: {e}")
            # placeholder
            self.title_image = self.title_font.render("TETRIS", True, COLOURS['white'])
            self.gameover_image = self.title_font.render("GAME OVER", True, COLOURS['white'])
            self.playbutton_images = {
                'normal': self.title_font.render("PLAY", True, COLOURS['white']),
                'hover': self.title_font.render("PLAY", True, COLOURS['yellow']),
                'click': self.title_font.render("PLAY", True, COLOURS['red']),
            }
    def draw_text(self, screen, text, font, colour, x, y, center=True):
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        screen.blit(text_surface, text_rect)

    def draw_start_screen(self, screen, button_state, flash_on):
        screen.fill(COLOURS['background'])

        # title
        title_rect = self.title_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(self.title_image, title_rect)

        # play button
        button_image = self.playbutton_images[button_state]
        if button_state == 'normal' and flash_on:
            # create white version for flashing
            white_button = button_image.copy()
            white_button.fill(COLOURS['white'], special_flags=pygame.BLEND_RGB_MAX)
            button_image = white_button
        
        button_rect = button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2/3))
        screen.blit(button_image, button_rect)
        return button_rect
    
    def draw_game_ui(self, screen, game):
        # draw side panel background
        panel_rect = pygame.Rect(SIDE_PANEL_X, PADDING, SIDE_PANEL_WIDTH, SIDE_PANEL_HEIGHT)
        pygame.draw.rect(screen, COLOURS['black'], panel_rect)

        # draw next pieces panel
        self.draw_text(screen, "NEXT", self.score_font, COLOURS['text'], SIDE_PANEL_X + SIDE_PANEL_WIDTH / 2, PADDING + 30)
        y_offset = PADDING + 80
        for i, piece in enumerate(game.next_pieces):
            self.draw_small_piece(screen, piece, SIDE_PANEL_X + SIDE_PANEL_WIDTH / 2, y_offset + i * 150)
        
        # draw score, lines, time
        info_y = SCORE_AREA_Y + 20
        self.draw_text(screen, f"SCORE: {game.score}", self.score_font, COLOURS['text'], SIDE_PANEL_X + 10, info_y + 40, center=False)
        self.draw_text(screen, f"LINES: {game.lines}", self.score_font, COLOURS['text'], SIDE_PANEL_X + 10, info_y + 40, center=False)

    def draw_small_piece(self, screen, piece, x_centre, y_centre):
        shape = piece.shape
        colour = piece.colour
        small_block_size = BLOCK_SIZE * 0.6

        start_x = x_centre - (len(shape[0] * small_block_size / 2))
        start_y = y_centre - (len(shape) * small_block_size / 2)

        for r_idx, row in enumerate(shape):
            for c_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, colour,
                                     (start_x + c_idx * small_block_size,
                                      start_y + r_idx * small_block_size,
                                      small_block_size - 2, small_block_size - 2))
    
    def draw_gameover_screen(self, screen, score, highscores, selected_option):
        screen.fill(COLOURS['background'])

        # gameover title
        title_rect = self.gameover_image.get_rect(center=(SCREEN_WIDTH // 2, 100))
        y_pos = 320
        for i, (scr, nme) in enumerate (highscores[:10]): # display top 10
            rank_text = f"{i+1}."
            name_text = nme
            score_text = str(scr)
            self.draw_text(screen, rank_text, self.score_font, COLOURS['text'], 250, y_pos, center=False)
            self.draw_text(screen, name_text, self.score_font, COLOURS['text'], 320, y_pos, center=False)
            self.draw_text(screen, score_text, self.score_font, COLOURS['text'], 650, y_pos, center=False)
            y_pos += 35

        # menu

        play_again_colour = COLOURS['yellow'] if selected_option == 0 else COLOURS['white']
        menu_colour = COLOURS['yellow'] if selected_option == 1 else COLOURS['white']

        play_again_rect = self.draw_text(screen, "PLAY AGAIN", self.menu_font, play_again_colour, SCREEN_WIDTH // 2, 700)
        menu_rect = self.draw_text(screen, "MENU", self.menu_font, menu_colour, SCREEN_WIDTH // 2, 770)

        return [play_again_rect, menu_rect]
    
    def draw_nameentry(self, screen, name, highscore):
        screen.fill(COLOURS['background'])
        self.draw_text(screen, "NEW HIGH SCORE!", self.menu_font, COLOURS['yellow'], SCREEN_WIDTH // 2, 250)
        self.draw_text(screen, f"YOUR SCORE: {highscore}", self.score_font, COLOURS['text'], SCREEN_WIDTH // 2, 250)
        self.draw_text(screen, "ENTER YOUR INITIALS (3 CHARS)", self.score_font, COLOURS['text'], SCREEN_WIDTH // 2, 350)

        # draw input box
        input_box = pygame.Rect(0, 0, 200, 60)
        input_box.center = (SCREEN_WIDTH // 2, 450)
        pygame.draw.rect(screen, COLOURS['white'], input_box, 2)
        
        self.draw_text(screen, name, self.input_font, COLOURS['white'], SCREEN_WIDTH // 2, 450)
        self.draw_text(screen, "PRESS ENTER TO CONFIRM", self.score_font, COLOURS['text'], SCREEN_WIDTH // 2, 550)
        
            
