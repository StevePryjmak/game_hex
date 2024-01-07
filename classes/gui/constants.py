import pygame
# Window constants
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
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


#  constant image for background
def blit_background(win):
    try:
        # Load and transform the background image
        bg_image = pygame.image.load("images/background_img3.jpg")
        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

        # Blit the image onto the window
        win.blit(bg_image, (0, 0))

    except pygame.error as e:
        print("Error can't blit the background:", e)
