# main.py
import pygame
import sys
from settings import *
from game import Game
from ui import UI
from highscores_manager import HighScoreManager

# game clasee

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.game_state = "START" # can be [START, PLAYING, NAME_ENTRY, GAMEOVER]

        # bgm
        try:
            pygame.mixer.music.load("tetris.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Could not load or play music: {e}")

        self.ui = UI()
        self.hs_manager = HighScoreManager()
        self.game = Game()

        # start screen specifics.
        self.play_button_rect = None
        self.play_button_state = "normal" # can be [normal, hover, click]
        self.flash_timer = 0
        self.flash_on = True

        # gameover screen specifics.
        self.gameover_selected_option = 0 # 0: play again, 1: menu

        # name entry specifics.
        self.playername = ""
        self.final_score = 0
        
        # --- CRT Effect Surfaces ---
        self.crt_scanlines = self._create_scanlines()
        self.crt_vignette = self._create_vignette()
        self.crt_curve_overlay = self._create_curve_overlay()

    # --- CRT Effect Helpers ---
    def _create_scanlines(self):
        """Creates a surface with semi-transparent horizontal lines."""
        scanlines = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
        for y in range(0, SCREEN_HEIGHT, 3):
            pygame.draw.line(scanlines, (0, 0, 0, 40), (0, y), (SCREEN_WIDTH, y), 1)
        return scanlines

    def _create_vignette(self):
        """Creates a surface with dark corners to simulate a vignette."""
        vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
        # Larger radius = softer vignette
        radius_x = int(SCREEN_WIDTH * 0.7)
        radius_y = int(SCREEN_HEIGHT * 0.7)
        
        for y in range(SCREEN_HEIGHT):
            for x in range(SCREEN_WIDTH):
                # Calculate distance from center, normalized
                dx = (x - SCREEN_WIDTH / 2) / radius_x
                dy = (y - SCREEN_HEIGHT / 2) / radius_y
                distance = dx*dx + dy*dy
                if distance > 0.3: # Start fading in past this distance
                    # Opacity increases the further from the center it is
                    alpha = min(255, int((distance - 0.3) * 250))
                    vignette.set_at((x, y), (0, 0, 0, alpha))
        return vignette

    def _create_curve_overlay(self):
        """Creates a black overlay that masks the screen into a convex shape."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(COLOURS['white']) # Use white as a colorkey
        
        # Draw a black rectangle that will become the overlay
        pygame.draw.rect(overlay, COLOURS['black'], (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Carve out the viewable "curved" area by drawing a white rounded rectangle
        viewable_area = pygame.Rect(5, 5, SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10)
        pygame.draw.rect(overlay, COLOURS['white'], viewable_area, border_radius=60)
        
        # Make the white part transparent, leaving only the black curved border
        overlay.set_colorkey(COLOURS['white'])
        return overlay

    def run(self):
        while True:
            # Delta time is not used in the original speed calculation, so we stick to a fixed FPS
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
                pygame.mixer.music.set_volume(0.2)
                self.handle_start_events(event)
            elif self.game_state == "PLAYING":
                pygame.mixer.music.set_volume(0.5)
                self.handle_playing_events(event)
            elif self.game_state == "NAME_ENTRY":
                self.handle_name_entry_events(event)
                pygame.mixer.music.set_volume(0.2)
            elif self.game_state == "GAMEOVER":
                self.handle_gameover_events(event)
                pygame.mixer.music.set_volume(0.1)

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
                    self.game_state = "GAMEOVER"
    
    def draw(self):
        # Step 1: Draw all the game content to the screen
        self.screen.fill(COLOURS["background"])
        if self.game_state == "START":
            self.play_button_rect = self.ui.draw_start_screen(self.screen, self.play_button_state, self.flash_on)
        elif self.game_state == "PLAYING":
            self.game.draw(self.screen)
            self.ui.draw_game_ui(self.screen, self.game)
        elif self.game_state == "NAME_ENTRY":
            self.ui.draw_nameentry(self.screen, self.playername, self.final_score)
        elif self.game_state == "GAMEOVER":
            self.ui.draw_gameover_screen(self.screen, self.final_score, self.hs_manager.scores, self.gameover_selected_option)

        # Step 2: Apply CRT effect layers on top of the drawn screen
        self.screen.blit(self.crt_scanlines, (0, 0))
        self.screen.blit(self.crt_vignette, (0, 0))
        self.screen.blit(self.crt_curve_overlay, (0, 0))

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
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.game.move_piece(-1, 0)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.game.move_piece(1, 0)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.game.move_piece(0, 1) # soft drop
                self.game.fall_time = 0 # reset timer, avoiding double drop
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.game.rotate_piece()
            elif event.key == pygame.K_SPACE:
                self.game.hard_drop()

    def handle_name_entry_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(self.playername) > 0:
                self.hs_manager.add_score(self.playername, self.final_score)
                self.game_state = "GAMEOVER"
            elif event.key == pygame.K_BACKSPACE:
                self.playername = self.playername[:-1]
            elif len(self.playername) < 10:
                # allow alphanumeric characters
                if event.unicode.isalnum():
                    self.playername += event.unicode.upper()

    def handle_gameover_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                self.gameover_selected_option = 1 - self.gameover_selected_option # Toggles between 0 and 1
            elif event.key in (pygame.K_z, pygame.K_RETURN):
                if self.gameover_selected_option == 0: # Option: Play Again
                    self.reset_game()
                    self.game_state = "PLAYING"
                else: # Option: Menu
                    self.reset_game()
                    self.game_state = "START"

if __name__ == '__main__':
    main_game = Main()
    main_game.run()