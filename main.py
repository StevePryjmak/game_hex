import time

import pygame
import sys
from classes.constants import WIDTH, HEIGHT, BG_COLOR, FIRST_PLAYER_COLOR, SECOND_PLAYER_COLOR, FONT, TEXT_COLOR
from classes.game import Game, GameBot, GameBotFirst
from classes.button import Button
from classes.start_menu import Menu, GameEndMenu
from pygame import Color
from classes.hexagon import Hexagon

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
        Button((WIDTH/2-100, HEIGHT/2+50), 200, 50, "Play with bot", select_color),
        Button((WIDTH / 2 - 100, HEIGHT / 2 + 150), 200, 50, "How to play", ),
        Button((WIDTH/2-100, HEIGHT/2+250), 200, 50, "Quit", quit_game)
    ]
    menu = Menu(buttons, win)
    menu.display_menu()


def sub_menu1():
    buttons = [
        Button((WIDTH / 2 - 100, HEIGHT / 2 - 50), 200, 50, "Play on 1 device", start_game, Game),
        Button((WIDTH / 2 - 100, HEIGHT / 2 + 50), 200, 50, "Play on different devices", main_menu, -1),
        # Second button not working jet
        Button((WIDTH / 2 - 100, HEIGHT / 2 + 150), 200, 50, "Back", main_menu, -1),
    ]
    menu = Menu(buttons, win)
    menu.display_menu()


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


def select_color():
    bg_image = pygame.image.load("images/background_img3.jpg")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    win.blit(bg_image, (0, 0))

    instruction_text = FONT.render(
        f'Choose color: {FIRST_PLAYER_COLOR[1]} goes first, {SECOND_PLAYER_COLOR[1]} goes second', True, TEXT_COLOR)
    instruction_text_rect = instruction_text.get_rect(center=(WIDTH / 2, HEIGHT / 3))
    win.blit(instruction_text, instruction_text_rect)

    bg_hexagon_left = Hexagon((0.25 * WIDTH, 0.75 * HEIGHT), HEIGHT * 0.11, 'grey')
    player_one_hex = Hexagon((0.25 * WIDTH, 0.75 * HEIGHT), HEIGHT * 0.1, FIRST_PLAYER_COLOR[0])
    bg_hexagon_left.draw(win)
    player_one_hex.draw(win)

    bg_hexagon_right = Hexagon((0.75 * WIDTH, 0.75 * HEIGHT), HEIGHT * 0.11, 'grey')
    player_two_hex = Hexagon((0.75 * WIDTH, 0.75 * HEIGHT), HEIGHT * 0.1, SECOND_PLAYER_COLOR[0])
    bg_hexagon_right.draw(win)
    player_two_hex.draw(win)

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONUP and player_one_hex.clicked(pygame.mouse.get_pos()):
                return start_game(GameBot)
            if event.type == pygame.MOUSEBUTTONUP and player_two_hex.clicked(pygame.mouse.get_pos()):
                return start_game(GameBotFirst)
        pygame.display.flip()


def start_game(game_mode):
    game = game_mode(win)
    run, pause, cord = True, False, False
    restart, menu = None, None
    while run:
        if game.game_ended:
            #  animate winner and open end_menu
            buttons = [
                Button((WIDTH / 2 - 100, HEIGHT / 2 - 50), 200, 50, "Main Menu", main_menu),
                Button((WIDTH / 2 - 100, HEIGHT / 2 + 50), 200, 50, "Play Again", start_game, game_mode)
            ]
            end_menu = GameEndMenu(buttons, game)
            if not end_menu.display_menu():
                return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause
                    if pause:
                        restart, menu = draw_pause()
                    else:
                        game.board.draw_board(win)
                    pygame.display.flip()

            if pause:
                if restart.clicked(event):
                    return start_game(game_mode)
                if menu.clicked(event):
                    return main_menu()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    game.update_mouse(pos)

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
