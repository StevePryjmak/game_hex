import pygame
# Window constants
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w/2, info.current_h/2
BG_COLOR = (50, 50, 50)
FPS = 20


#  Buttons constants
BTN_COLOR = (0, 0, 255)  # (0, 120, 215)
HOVER_COLOR = (50, 100, 255)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.SysFont('8-BIT WONDER.TTF', int(min(HEIGHT, WIDTH)*0.06))
BTN_WIDTH = WIDTH/4
BTN_HEIGHT = HEIGHT/12
BTN_OFFSET = BTN_HEIGHT*1.4

# board and player constants
FIRST_PLAYER_COLOR = (255, 0, 0), 'Red'
SECOND_PLAYER_COLOR = (0, 0, 255), 'Blue'

