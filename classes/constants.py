import pygame
# Window constants
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h-70
BG_COLOR = (50, 50, 50)


# Buttons constants
BTN_COLOR = (0, 120, 215)
HOVER_COLOR = (0, 150, 255)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.SysFont('Arial', 25)
