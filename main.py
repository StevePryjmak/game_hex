import pygame
import sys
from classes.constants import WIDTH, HEIGHT, FIRST_PLAYER_COLOR, SECOND_PLAYER_COLOR, FONT, TEXT_COLOR, FPS
from classes.constants import blit_background, BTN_WIDTH, BTN_HEIGHT, BTN_OFFSET
from classes.game import Game, GameBot, GameBotFirst
from classes.network import Server, Client
from classes.button import Button
from classes.start_menu import Menu, GameEndMenu, SelectNetworkMenu, OpponentAbandonedGameMenu
from classes.hexagon import Hexagon

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))

#  win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption('Hex')
clock = pygame.time.Clock()


def quit_game():
    pygame.quit()
    sys.exit()


def main_menu():
    buttons_x, buttons_y = (WIDTH - BTN_WIDTH) / 2, (HEIGHT - BTN_HEIGHT) / 2
    buttons = [
        Button((buttons_x, buttons_y), BTN_WIDTH, BTN_HEIGHT, "Play with friend", friend_game_menu, ),
        Button((buttons_x, buttons_y + BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Play with bot", select_color),
        Button((buttons_x, buttons_y + 2*BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "How to play", ),
        Button((buttons_x, buttons_y + 3*BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Quit", quit_game)
    ]
    menu = Menu(buttons, win)
    menu.display_menu()
    quit_game()


def friend_game_menu():
    buttons_x, buttons_y = (WIDTH - BTN_WIDTH) / 2, (HEIGHT - BTN_HEIGHT) / 2
    buttons = [
        Button((buttons_x, buttons_y), BTN_WIDTH, BTN_HEIGHT, "Play on 1 device", start_game, Game),
        Button((buttons_x, buttons_y + BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Play on 2 devices", select_mod,),
        Button((buttons_x, buttons_y + 2*BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Back", main_menu,),
    ]
    menu = Menu(buttons, win)
    menu.display_menu()
    quit_game()


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
    blit_background(win)

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
    quit_game()


def start_game(game_mode):
    game = game_mode(win)
    run, pause, cord = True, False, False
    restart, menu = None, None
    main_buttons = [
        Button((WIDTH*0.93, 0.02*HEIGHT), 0.05*WIDTH, 0.05*WIDTH, img='images/white-home-icon.png'),
        Button((0, HEIGHT * 0.85),  HEIGHT * 0.15, HEIGHT * 0.15, img='images/undo1.png')
    ]
    for button in main_buttons:
        button.draw(win)
    while run:
        if game.game_ended:
            #  animate winner and open end_menu
            buttons_x, buttons_y = (WIDTH - BTN_WIDTH) / 2, (HEIGHT - BTN_HEIGHT) / 2
            end_buttons = [
                Button((buttons_x, buttons_y), BTN_WIDTH, BTN_HEIGHT, "Main Menu", main_menu),
                Button((buttons_x, buttons_y + BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Play Again", start_game, game_mode)
            ]
            end_menu = GameEndMenu(end_buttons, game, True, main_buttons[1])
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
            if event.type == pygame.MOUSEBUTTONUP:
                if main_buttons[0].clicked(event):
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
                    if main_buttons[1].rect.collidepoint(pos):
                        game.revert_move(pos)
                    game.update_mouse(pos)

                if not game.game_ended:
                    game.draw_dot(pygame.mouse.get_pos())

                    main_buttons[1].clicked(event)
                    for button in main_buttons:
                        button.draw(win)

        pygame.display.flip()
        clock.tick(FPS)
    quit_game()


def select_mod():
    buttons_x, buttons_y = (WIDTH - BTN_WIDTH) / 2, (HEIGHT - BTN_HEIGHT) / 2
    buttons = [
        Button((buttons_x, buttons_y), BTN_WIDTH, BTN_HEIGHT, "Server", play_on_2_devices, 'server'),
        Button((buttons_x, buttons_y + BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Client", play_on_2_devices, 'client'),
        Button((buttons_x, buttons_y + 2*BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Back", friend_game_menu)
    ]
    menu = SelectNetworkMenu(buttons, win)
    menu.display_menu()
    quit_game()


def play_on_2_devices(mode):
    # Determine if running as server or client based on mode
    device = Server(win) if mode == 'server' else Client(win)
    try:
        running = True
        while running:
            if device.game and device.game.game_ended:
                #  animate winner and open end_menu
                device.shutdown_event.set()
                buttons_x, buttons_y = (WIDTH - BTN_WIDTH) / 2, (HEIGHT - BTN_HEIGHT) / 2
                end_buttons = [
                    Button((buttons_x, buttons_y), BTN_WIDTH, BTN_HEIGHT, "Main Menu", main_menu),
                    Button((buttons_x, buttons_y + BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Leave Game", quit_game)
                ]
                end_menu = GameEndMenu(end_buttons, device.game)
                end_menu.display_menu()

            if device.game_aborted:
                raise ConnectionAbortedError
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    device.shutdown_event.set()  # Signal all threads to shut down
                    break
                if not device.socket:
                    pass
                elif not device.game:
                    device.game = Game(win)
                elif event.type == pygame.MOUSEBUTTONUP and not device.waiting_for_msg:
                    pos = pygame.mouse.get_pos()
                    if device.game.update_mouse(pos):
                        message = f"{pos}"
                        device.socket.sendall(message.encode())
                        device.waiting_for_msg = True
                elif not device.waiting_for_msg and not device.game.game_ended:
                    pos = pygame.mouse.get_pos()
                    device.game.draw_dot(pos)
                    message = f"N{pos}"
                    device.socket.sendall(message.encode())
            pygame.display.flip()
            clock.tick(FPS)

    except KeyboardInterrupt:
        # Handle the CTRL+C interrupt
        device.shutdown_event.set()
    except ConnectionAbortedError:
        #  pass for now but not forgot to add menu and return to main menu option
        buttons_x, buttons_y = (WIDTH - BTN_WIDTH) / 2, (HEIGHT - BTN_HEIGHT) / 2
        buttons = [
            Button((buttons_x, buttons_y), BTN_WIDTH, BTN_HEIGHT, "Main Menu", main_menu),
            Button((buttons_x, buttons_y + BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Leave Game", quit_game)
        ]
        menu = OpponentAbandonedGameMenu(buttons, win)
        menu.display_menu()
        print("Abandoned")
    finally:
        # Clean up on close
        if device.socket:
            device.socket.close()
        if mode == 'server':
            device.server_socket.close()
        quit_game()


if __name__ == '__main__':
    main_menu()
