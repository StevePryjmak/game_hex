import pygame
# Window constants
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
BG_COLOR = (50, 50, 50)


# Buttons constants
BTN_COLOR = (0, 120, 215)
HOVER_COLOR = (0, 150, 255)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.SysFont('8-BIT WONDER.TTF', 30)

# board and player constants
FIRST_PLAYER_COLOR = (255, 0, 0), 'Red'
SECOND_PLAYER_COLOR = (0, 0, 255), 'Blue'
