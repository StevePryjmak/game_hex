import pygame
import sys
from classes.gui.constants import WIDTH, HEIGHT, FIRST_PLAYER_COLOR, SECOND_PLAYER_COLOR, FONT, TEXT_COLOR, FPS
from classes.gui.constants import blit_background, BTN_WIDTH, BTN_HEIGHT, BTN_OFFSET
from classes.game import Game, GameBot, GameBotFirst
from classes.network import Server, Client
from classes.gui.button import Button
from classes.gui.menus import Menu, GameEndMenu, SelectNetworkMenu, OpponentAbandonedGameMenu, ShowInstruction
from classes.gui.hexagon import Hexagon
from classes.gui.gui_board import GuiBoard

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
        Button((buttons_x, buttons_y + 2*BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "How to play", show_instruction),
        Button((buttons_x, buttons_y + 3*BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Quit", quit_game)
    ]
    menu = Menu(buttons, win)
    menu.display_menu()
    quit_game()


def show_instruction():
    buttons_x, buttons_y = (WIDTH - BTN_WIDTH) / 2, (HEIGHT - BTN_HEIGHT) / 2
    buttons = [Button((buttons_x, buttons_y + 3*BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Back", main_menu,)]
    menu = ShowInstruction(buttons,win)
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
    offset = 0.3
    buttons_x, buttons_y = (offset*WIDTH, offset*HEIGHT)
    width, height = (1-2*offset)*WIDTH, 0.08*HEIGHT
    resume = Button((buttons_x, buttons_y), width, height,
                    'Game Paused: Escape to Resume', color='dark grey', border_radius=height*0.2)
    restart = Button((buttons_x, buttons_y + height*1.1), width/2*0.9, height,
                     'Restart', color='black', border_radius=height*0.2)
    menu = Button((buttons_x + width/2*1.1, buttons_y + height*1.1), width/2*0.9, height,
                  'Menu', color='blue', border_radius=height*0.2)
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
    game = game_mode()
    gui_board = GuiBoard(win)
    gui_board.update_board(game.board.cells)
    gui_board.draw_board(win)
    run, pause, coordinates = True, False, False
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
            end_menu = GameEndMenu(end_buttons, game, True, main_buttons[1], gui_board)
            if not end_menu.display_menu():
                return
            gui_board.draw_board(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause
                    if pause:
                        restart, menu = draw_pause()
                    else:
                        gui_board.draw_board(win)
                    pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONUP:
                if main_buttons[0].clicked(event):
                    pause = not pause
                    if pause:
                        restart, menu = draw_pause()
                    else:
                        gui_board.draw_board(win)
                        for button in main_buttons:
                            button.draw(win)
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
                        game.revert_move()
                        gui_board.update_board(game.board.cells)
                    i, j = gui_board.get_hex_cords(pos)
                    if i == -1 or gui_board.hex_cells[i][j].used:
                        continue
                    if game.handle_move(i, j):
                        gui_board.update_board(game.board.cells)

                if not game.game_ended:
                    pos = pygame.mouse.get_pos()
                    gui_board.draw_dot(pos, game.player1_turn)

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
        Button((buttons_x, buttons_y + BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Input host to connect", input_host),
        Button((buttons_x, buttons_y + 2*BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Connect to local host",
               play_on_2_devices, 'client'),
        Button((buttons_x, buttons_y + 3*BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Back", friend_game_menu)
    ]
    menu = SelectNetworkMenu(buttons, win)
    menu.display_menu()
    quit_game()


def input_host():

    text = ''
    rect_width = WIDTH*0.2
    rect_height = HEIGHT*0.06
    input_box = pygame.Rect((WIDTH-rect_width)/2, (HEIGHT-rect_height)/2, rect_width, rect_height)
    buttons_x, buttons_y = (WIDTH - BTN_WIDTH) / 2, (HEIGHT - BTN_HEIGHT) / 2
    buttons = [
        Button((WIDTH/2, HEIGHT/3), 0, 0, 'Write ip here to connect'),
        Button((buttons_x, buttons_y + 3 * BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Back", select_mod)
    ]

    def update_screen():

        win.fill((0, 0, 0))

        txt_surface = FONT.render(text, True, TEXT_COLOR)
        width = max(WIDTH*0.2, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text
        win.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(win, (255, 255, 255), input_box, 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_RETURN:
                    return play_on_2_devices('client', text)
                else:
                    text += event.unicode
                update_screen()
            for button in buttons:
                if button.clicked(event):
                    button.execute_funk()
        for button in buttons:
            button.draw(win)
        pygame.display.flip()
        update_screen()


def play_on_2_devices(mode, external_ip=False):

    def clear_all():
        device.shutdown_event.set()
        if device.socket:
            device.socket.close()
        if mode == 'server':
            device.server_socket.close()


    # Determine if running as server or client based on mode
    if external_ip:
        device = Client(win, external_ip)
    else:
        device = Server(win) if mode == 'server' else Client(win)
    win.fill((0, 0, 0))
    Button((WIDTH / 2, HEIGHT / 3), 0, 0, 'Waiting for connection').draw(win)
    leave_button = Button((WIDTH * 0.93, 0.02 * HEIGHT), 0.05 * WIDTH, 0.05 * WIDTH, img='images/cancel.png')
    try:
        running = True
        while running:
            if device.game and device.game.game_ended:
                #  animate winner and open end_menu
                clear_all()
                buttons_x, buttons_y = (WIDTH - BTN_WIDTH) / 2, (HEIGHT - BTN_HEIGHT) / 2
                end_buttons = [
                    Button((buttons_x, buttons_y), BTN_WIDTH, BTN_HEIGHT, "Main Menu", main_menu),
                    Button((buttons_x, buttons_y + BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Leave Game", quit_game)
                ]
                end_menu = GameEndMenu(end_buttons, device.game, gui_board=device.gui_board)
                end_menu.display_menu()

            if device.game_aborted:
                raise ConnectionAbortedError
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    device.shutdown_event.set()  # Signal all threads to shut down
                    break
                if device.game and event.type == pygame.MOUSEBUTTONUP:
                    if leave_button.rect.collidepoint(pygame.mouse.get_pos()):
                        clear_all()
                        return main_menu()
                if not device.socket:
                    buttons_x, buttons_y = (WIDTH - BTN_WIDTH) / 2, (HEIGHT - BTN_HEIGHT) / 2
                    back_button = Button((buttons_x, buttons_y + 3 * BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT,
                                         "Back", select_mod)
                    back_button.draw(win)
                    if back_button.clicked(event):
                        clear_all()
                        back_button.execute_funk()
                elif not device.game:
                    device.game = Game()
                    device.gui_board = GuiBoard(win)
                    device.gui_board.draw_board(win)
                    leave_button.draw(win)
                elif event.type == pygame.MOUSEBUTTONUP and not device.waiting_for_msg:
                    pos = pygame.mouse.get_pos()
                    i, j = device.gui_board.get_hex_cords(pos)
                    if i == -1 or device.gui_board.hex_cells[i][j].used:
                        continue

                    if device.game.handle_move(i, j):
                        device.gui_board.update_board(device.game.board.cells)
                        message = f"{pos}"
                        device.socket.sendall(message.encode())
                        device.waiting_for_msg = True
                elif not device.waiting_for_msg and not device.game.game_ended:
                    pos = pygame.mouse.get_pos()
                    device.gui_board.draw_dot(pos, device.game.player1_turn)
                    message = f"N{pos}"
                    device.socket.sendall(message.encode())


            pygame.display.flip()
            clock.tick(FPS)

    except KeyboardInterrupt:
        # Handle the CTRL+C interrupt
        device.shutdown_event.set()
    except ConnectionAbortedError:
        #  pass for now but not forgot to add menu and return to main menu option
        clear_all()
        buttons_x, buttons_y = (WIDTH - BTN_WIDTH) / 2, (HEIGHT - BTN_HEIGHT) / 2
        buttons = [
            Button((buttons_x, buttons_y), BTN_WIDTH, BTN_HEIGHT, "Main Menu", main_menu),
            Button((buttons_x, buttons_y + BTN_OFFSET), BTN_WIDTH, BTN_HEIGHT, "Leave Game", quit_game)
        ]
        menu = OpponentAbandonedGameMenu(buttons, win)
        menu.display_menu()
        print("Abandoned")
        return
    finally:
        # Clean up on close
        clear_all()
        quit_game()


if __name__ == '__main__':
    main_menu()
