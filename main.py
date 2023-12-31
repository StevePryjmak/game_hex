import time

import pygame
import sys
from classes.constants import WIDTH, HEIGHT, BG_COLOR, FIRST_PLAYER_COLOR, SECOND_PLAYER_COLOR
from classes.game import Game, GameBot
from classes.button import Button
from classes.start_menu import Menu
from pygame import Color

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))

#win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
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
    menu.display_menu(win)


def sub_menu1():
    buttons = [
        Button((WIDTH / 2 - 100, HEIGHT / 2 - 50), 200, 50, "Play on 1 device", start_game, 'Game'),
        Button((WIDTH / 2 - 100, HEIGHT / 2 + 50), 200, 50, "Play on different devices", main_menu, -1),
        # Second button not working jet
        Button((WIDTH / 2 - 100, HEIGHT / 2 + 150), 200, 50, "Back", main_menu, -1),
    ]
    menu = Menu(buttons, win)
    menu.display_menu(win)


def draw_pause():
    pygame.draw.rect(surface, (128, 128, 128, 120), [0, 0, WIDTH, HEIGHT])
    resume = Button((200, 150), 600, 50, 'Game Paused: Escape to Resume', color='dark grey', border_radius=10)
    restart = Button((200, 250), 250, 50, 'Restart', color='black', border_radius=10)
    menu = Button((500, 250), 250, 50, 'Menu', color='blue', border_radius=10)
    win.blit(surface, (0, 0))
    resume.draw(win)
    restart.draw(win)
    menu.draw(win)
    return restart, menu


def start_game(game_mod):
    game = Game(win) if game_mod == 'Game' else GameBot(win)
    run = True
    pause = False
    restart, menu = None, None
    cord = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False if pause else True
                    if pause:
                        restart, menu = draw_pause()
                    else:
                        game.board.draw_board(win)
                    pygame.display.flip()
            if pause:
                if restart.clicked(event):
                    return start_game(game_mod)
                if menu.clicked(event):
                    return main_menu()

                continue
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                game.update_mouse(pos)
            #  draw circle on hexagon when mouse in on top
            if not game.game_ended:
                color = FIRST_PLAYER_COLOR[0] if game.player1_turn else SECOND_PLAYER_COLOR[0]
                cord = game.board.highlight_hex_cell(win, color, cord)

            game.board.back_button.clicked(event)
            game.board.back_button.draw(win)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main_menu()
