import pygame

pygame.init()

screen = pygame.display.set_mode((900, 850))
clock = pygame.time.Clock()
running = True

while running:
    pygame.display.flip()
    clock.tick(60)

pygame.quit()