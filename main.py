import pygame
from classes.constants import WIDTH, HEIGHT
from classes.game import Game, GameBot


pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hex')
game = Game(WIN)
done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            game.update_mouse(pos)


pygame.quit()
