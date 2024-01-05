import pygame
import socket
import threading
import urllib.request
from classes.constants import HEIGHT, WIDTH, blit_background, FONT, TEXT_COLOR


class NetworkEntity:
    def __init__(self, win):
        self.win = win
        self.game = None  # Will create game object when needed
        self.waiting_for_msg = False
        self.host = 'localhost'
        self.port = 55555
        self.socket = None
        self.server_socket = None
        self.game_aborted = False
        self.shutdown_event = threading.Event()

    def setup_connection(self, as_server=False):
        if as_server:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.server_socket.setblocking(False)
        else:
            self.socket = self.attempt_connect()
            if self.socket:
                thread = threading.Thread(target=self.handle_communication)
                thread.start()

    def attempt_connect(self):
        while not self.shutdown_event.is_set():
            try:
                temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                temp_socket.connect((self.host, self.port))
                temp_socket.setblocking(False)
                print("Connected to server!")
                return temp_socket
            except socket.error:
                print("Connection attempt failed, trying again...")
                if self.shutdown_event.wait(2):
                    return None

    def display_info(self, message):
        try:
            blit_background(self.win)
            instruction_text = FONT.render(message, True, TEXT_COLOR)
            instruction_text_rect = instruction_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            self.win.blit(instruction_text, instruction_text_rect)
        except pygame.error:
            # This issue may occur if the client is already waiting, but the server has only just been created.
            # Consequently, the game begins in a brief period during which the previous window has already closed.
            # However, the game attempts to execute a blit operation on the previous window
            # because the function was originally called in the context of the previous window.

            #  #Double comment this issue probably occur because game class was cretin in threading and because of  that
            #  It created a lot of different bugs
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
                        self.game.draw_dot(mouse_pos)
                        continue
                    elif mouse_pos:
                        mouse_pos = mouse_pos.strip('()').split(',')
                        mouse_pos = (int(mouse_pos[0]), int(mouse_pos[1]))
                        print(mouse_pos)
                        self.game.update_mouse(mouse_pos)
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
        connection_thread = threading.Thread(target=self.setup_connection(as_server=True))
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
    def __init__(self, win):
        super().__init__(win)
        self.waiting_for_msg = True
        self.setup_connection()

    def start_client(self):
        connection_thread = threading.Thread(target=self.setup_connection())
        connection_thread.start()
