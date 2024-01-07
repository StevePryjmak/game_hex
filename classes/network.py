import pygame
import socket
import threading
import urllib.request
from classes.gui.constants import HEIGHT, WIDTH, blit_background, FONT, TEXT_COLOR


class NetworkEntity:
    def __init__(self, win):
        self.win = win
        self.game = None  # Will create game object when needed
        self.gui_board = None
        self.waiting_for_msg = False
        self.host = 'localhost'
        self.port = 55555
        self.socket = None
        self.server_socket = None
        self.game_aborted = False
        self.shutdown_event = threading.Event()

    def setup_connection(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.server_socket.setblocking(False)

    def attempt_connect(self):
        while not self.shutdown_event.is_set():
            try:
                temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                temp_socket.connect((self.host, self.port))
                temp_socket.setblocking(False)
                print("Connected to server!")
                self.socket = temp_socket
                thread1 = threading.Thread(target=self.handle_communication)
                thread1.start()
                break
            except socket.error:
                print("Connection attempt failed, trying again...")
                # if self.shutdown_event.wait(2):
                #     return None

    def display_info(self, message):
        try:
            blit_background(self.win)
            instruction_text = FONT.render(message, True, TEXT_COLOR)
            instruction_text_rect = instruction_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            self.win.blit(instruction_text, instruction_text_rect)
        except pygame.error:
            print('Pygame.error')

    def handle_communication(self):
        while not self.shutdown_event.is_set():
            if self.waiting_for_msg:
                try:
                    mouse_pos = self.socket.recv(1024).decode()
                    if not mouse_pos:
                        self.game_aborted = True
                        break
                    if mouse_pos[0] == 'N':
                        mouse_pos = mouse_pos.strip('N()').split(',')
                        mouse_pos = (int(mouse_pos[0]), int(mouse_pos[1]))
                        self.gui_board.draw_dot(mouse_pos, self.game.player1_turn)
                        continue
                    elif mouse_pos:
                        mouse_pos = mouse_pos.strip('()').split(',')
                        mouse_pos = (int(mouse_pos[0]), int(mouse_pos[1]))
                        print(mouse_pos)
                        i, j = self.gui_board.get_hex_cords(mouse_pos)
                        if i == -1 or self.gui_board.hex_cells[i][j].used:
                            continue
                        self.game.handle_move(i, j)
                        self.gui_board.update_board(self.game.board.cells)
                        if self.game.game_ended:
                            self.shutdown_event.set()
                            break
                        print("Received:", mouse_pos)
                        self.waiting_for_msg = False
                except BlockingIOError:
                    pass
                except ValueError:
                    print("Got wrong message")
                    pass


class Server(NetworkEntity):
    def __init__(self, win):
        super().__init__(win)
        self.waiting_for_msg = False
        self.external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        self.start_server()
        self.wait_for_connection()

    def start_server(self):
        connection_thread = threading.Thread(target=self.setup_connection)
        connection_thread.start()

    def wait_for_connection(self):
        connection_thread = threading.Thread(target=self.accept_connection)
        connection_thread.start()

    def accept_connection(self):
        self.display_info(f'Send this IP: {self.external_ip} to your friend to connect him to game')
        while not self.shutdown_event.is_set():
            if not self.server_socket:
                continue
            try:
                self.socket, address = self.server_socket.accept()
                print(f"Connected to {address}")
                thread = threading.Thread(target=self.handle_communication)
                thread.start()
                break
            except BlockingIOError:
                continue
            except OSError:
                pass


class Client(NetworkEntity):
    def __init__(self, win, host=None):
        super().__init__(win)
        self.waiting_for_msg = True
        if host:
            self.host = host
        self.start_client()

    def start_client(self):
        connection_thread = threading.Thread(target=self.attempt_connect)
        connection_thread.start()
