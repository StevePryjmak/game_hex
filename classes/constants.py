import pygame
# Window constants
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w/2, info.current_h/2
BG_COLOR = (50, 50, 50)
FPS = 10



# Buttons constants
BTN_COLOR = (0, 120, 215)
HOVER_COLOR = (0, 150, 255)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.SysFont('8-BIT WONDER.TTF', 30)

# board and player constants
FIRST_PLAYER_COLOR = (255, 0, 0), 'Red'
SECOND_PLAYER_COLOR = (0, 0, 255), 'Blue'


#  constant image for background
def blit_background(win):
    bg_image = pygame.image.load("images/background_img3.jpg")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    win.blit(bg_image, (0, 0))
