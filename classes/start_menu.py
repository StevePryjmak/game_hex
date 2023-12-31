import pygame
import sys
from classes.constants import WIDTH, HEIGHT
from classes.button import Button
from classes.constants import WIDTH, HEIGHT, BG_COLOR


class Menu:
    def __init__(self, buttons, win):
        self.buttons = buttons
        self.win = win

    def display_menu(self, win):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in self.buttons:
                    if button.clicked(event):
                        # if button == self.buttons[0]:
                        #     return  # Return the next menu function
                        # elif button == self.buttons[1]:
                        #     return  # Return the next menu function
                        # elif button == self.buttons[2]:
                        #     pygame.quit()
                        #     sys.exit()
                        button.execute_funk()

            self.win.fill(BG_COLOR)  # Need exeperiment with different colors
            background_image = pygame.image.load("images/background_img3.jpg")
            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
            win.blit(background_image, (0, 0))
            for button in self.buttons:
                button.draw(self.win)
            pygame.display.flip()






