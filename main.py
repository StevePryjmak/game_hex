import pygame
import sys
from classes.constants import WIDTH, HEIGHT, BG_COLOR
from classes.game import Game, GameBot
from classes.button import Button
from classes.start_menu import Menu

pygame.init()
#win = pygame.display.set_mode((WIDTH, HEIGHT))

win = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
pygame.display.set_caption('Hex')


def quit_game():
    pygame.quit()
    sys.exit()


def main_menu():
    buttons = [
        Button((WIDTH/2-100, HEIGHT/2-50), 200, 50, "Play with friend", sub_menu1, -1),
        Button((WIDTH/2-100, HEIGHT/2+50), 200, 50, "Play with bot", start_game, 'GameBot'),
        Button((WIDTH / 2 - 100, HEIGHT / 2 + 150), 200, 50, "How to play", ),
        Button((WIDTH/2-100, HEIGHT/2+250), 200, 50, "Quit", quit_game)
    ]
    menu = Menu(buttons, win)
    menu.display_menu()


def sub_menu1():
    buttons = [
        Button((WIDTH / 2 - 100, HEIGHT / 2 - 50), 200, 50, "Play on 1 device", start_game, 'Game'),
        Button((WIDTH / 2 - 100, HEIGHT / 2 + 50), 200, 50, "Play on different devices", main_menu, -1),
        # Second button not working jet
        Button((WIDTH / 2 - 100, HEIGHT / 2 + 150), 200, 50, "Back", main_menu, -1),
    ]
    menu = Menu(buttons, win)
    menu.display_menu()


def start_game(game):
    game = Game(win) if game == 'Game' else GameBot(win)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                game.update_mouse(pos)
            game.board.back_button.clicked(event)
            game.board.back_button.draw(win)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main_menu()
