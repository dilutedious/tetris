import pygame
import sys
from settings import *
from game import Game
from ui import UI
from highscores_manager import HighScoreManager

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.game_state = "START" # can be [start, playing, name_entry, gameover]

        self.ui = UI()
        self.hs_manager = HighScoreManager()
        self.game = Game()

        # start screen specifics.
        self.play_button_rect = None
        self.play_button_state = "noraml" # can be [normal, hover, click]
        self.flash_timer = 0
        self.flash_on = True

        # gameover screen specifics.
        self.gameover_selected_option = 0 # 0: play again, 1: meu

        # name entry specifics.
        self.playername = ""
        self.final_score = 0

    def run(self):
        while True:
            dt = self.clock.tick(60)

            self.handle_events()
            self.update(dt)
            self.draw()

            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.game_state == "START":
                self.handle_start_events(event)
            if self.game_state == "PLAYING":
                self.handle_playing_events(event)
            if self.game_state == "NAME_ENTRY":
                self.handle_name_entry_events(event)
            if self.game_state == "GAMEOVER":
                self.handle_gameover_events(event)

    def update(self, dt):
        if self.game_state == "START":
            self.flash_timer += dt
            if self.flash_timer >= 500:
                self.flash_timer = 0
                self.flash_on = not self.flash_on
        elif self.game_state == "PLAYING":
            self.game.update(dt)
            if self.game.game_over:
                self.final_score = self.game.score
                if self.hs_manager.ishighscore(self.final_score):
                    self.game_state = "NAME_ENTRY"
                else:
                    self.game_state = "GAME_OVER"
    
    def draw(self):
        self.screen.fill(COLOURS["background"])
        if self.game_state == "START":
            self.play_button_rect = self.ui.draw_start_screen(self.screen, self.play_button_state, self.flash_on)
        elif self.game_state == "PLAYING":
            self.game.draw(self.screen)
            self.ui.draw_game_ui(self.screen, self.game)
        elif self.game_state == "NAME_ENTRY":
            self.ui.draw_nameentry(self.screen, self.playername, self.final_score)
        elif self.game_state == "GAME_OVER":
            self.ui.draw_gameover_screen(self.screen, self.final_score, self.hs_manager.scores, self.gameover_selected_option)

    def reset_game(self):
        self.game = Game()
        self.playername = ""
        self.final_score = 0
        self.gameover_selected_option = 0

    def handle_start_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button_rect and self.play_button_rect.collidepoint(mouse_pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.play_button_state = "click"
            elif event.type == pygame.MOUSEBUTTONUP:
                self.reset_game()
                self.game_state = "PLAYING"
                self.play_button_state = "hover"
            else:
                self.play_button_state = "hover"
        else:
            self.play_button_state = "normal"

    def handle_playing_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.game.move_piece(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.game.move_piece(1, 0)
            elif event.key == pygame.K_DOWN:
                self.game.move_piece(0, 1) # soft drop
                self.game.fall_time = 0 # reset timer, avoidngi double drop
            elif event.key == pygame.K_UP:
                self.game.rotate_piece()
            elif event.key == pygame.K_SPACE:
                self.game.hard_drop()

    def handle_name_entry_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(self.playername) > 0:
                self.hs_manager.add_score(self.playername, self.final_score)
                self.game_state = "GAME_OVER"
            elif event.key == pygame.K_BACKSPACE:
                self.playername = self.playername[:-1]
            elif len(self.playername) < 10:
                # allow alphanumeric characters
                if event.unicode.isalnum():
                    self.playername += event.unicode.upper()

    def handle_gameover_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.gameover_selected_option = (self.gameover_selected_option - 1) % 2 # odd or even
            elif event.key == pygame.K_DOWN:
                self.gameover_selected_option = (self.gameover_selected_option + 1) % 2
            elif event.key in (pygame.K_z, pygame.K_RETURN):
                if self.gameover_selected_option == 0:
                    self.reset_game()
                else:
                    pygame.quit()
                    sys.exit()

# ———————————

main_game = Main()
main_game.run()

            