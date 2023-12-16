import pygame
from .constants import WIDTH,HEIGHT
from .button import Button


class Menu:
    def __init__(self):
        self.start_button = Button((1, 50, 32), WIDTH / 2 - 50, HEIGHT / 2 - 25, 100, 50, 'Start')

    def draw_menu(self, win):
        background_image = pygame.image.load("classes/background.jpg")
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        win.blit(background_image, (0, 0))
        self.start_button.draw(win)
        pygame.display.flip()

