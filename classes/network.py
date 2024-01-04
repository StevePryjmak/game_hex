import pygame
import socket
import threading
import urllib.request
from classes.game import Game
from classes.constants import HEIGHT, WIDTH, blit_background, FONT, TEXT_COLOR


class Server:
    # Game on different devises and Game against bot basicly the same program only needed move from opponent
    # I wanted to do Game with bot parent and move from there but i came up with another idea to start game object when
    # client connects
    def __init__(self, win):
        self.win = win
        self.game = None  # Will create game object when someone connects
        self.waiting_for_msg = False
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        self.port = 55555
        self.external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8') # I want to use it to connect from another
        # device but for now in doing nothing because host i local and connection is also local
        self.connection = None # This will hold the client connection
        self.setup_server()
        self.shutdown_event = threading.Event()
        self.wait_for_connection()

    # Network setup
    def setup_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        self.server_socket.setblocking(False)
        print("Server is listening...")

    def wait_for_connection(self):
        connection_thread = threading.Thread(target=self.accept_connection)
        connection_thread.start()

    def accept_connection(self):
        self.display_info()
        while not self.shutdown_event.is_set():
            try:
                self.connection, address = self.server_socket.accept()
                print(f"Connected to {address}")
                self.wait_for_opponent_move()
                break
            except BlockingIOError:
                continue

    def display_info(self):
        blit_background(self.win)
        instruction_text = FONT.render(
            f'Send this IP: {self.external_ip} to your friend connect him to game', True, TEXT_COLOR)
        instruction_text_rect = instruction_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.win.blit(instruction_text, instruction_text_rect)
        instruction_text = FONT.render(
            f' Server waiting for connection...', True, TEXT_COLOR)
        instruction_text_rect = instruction_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))
        self.win.blit(instruction_text, instruction_text_rect)

    def wait_for_opponent_move(self):
        client_thread = threading.Thread(target=self.handle_client)
        client_thread.start()

    def handle_client(self):
        self.game = Game(self.win)
        while not self.shutdown_event.is_set():
            while not self.connection:
                if self.shutdown_event.is_set():
                    return
                continue

            if self.waiting_for_msg:
                try:
                    mouse_pos = self.connection.recv(1024).decode()
                    mouse_pos = mouse_pos.strip('()').split(',')
                    mouse_pos = (int(mouse_pos[0]), int(mouse_pos[1]))

                    self.game.update_mouse(mouse_pos)
                    if mouse_pos:
                        print("Received:", mouse_pos)
                        self.waiting_for_msg = False
                except BlockingIOError:
                    pass

class Client():
    def __init__(self, win):
        self.win = win
        self.game = None
        self.host = 'localhost'
        self.port = 55555
        self.waiting_for_msg = True
        self.client_socket = None
        self.shutdown_event = threading.Event()
        connection_thread = threading.Thread(target=self.start_connection)
        connection_thread.start()

    def attempt_connect(self):
        while not self.shutdown_event.is_set():
            try:
                temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                temp_socket.connect((self.host, self.port))
                temp_socket.setblocking(0)
                print("Connected to server!")
                return temp_socket
            except socket.error as e:
                print("Connection attempt failed, trying again...")
                if self.shutdown_event.wait(2):
                    return None

    def start_connection(self):
        self.client_socket = self.attempt_connect()
        if self.client_socket and not self.shutdown_event.is_set():
            self.game = Game(self.win)
            thread = threading.Thread(target=self.handle_server)
            thread.start()

    def handle_server(self):
        self.game = Game(self.win)
        while not self.shutdown_event.is_set() and self.client_socket:

            if self.waiting_for_msg:
                try:

                    mouse_pos = self.client_socket.recv(1024).decode()
                    mouse_pos = mouse_pos.strip('()').split(', ')

                    mouse_pos = (int(mouse_pos[0]), int(mouse_pos[1]))
                    print(mouse_pos)
                    self.game.update_mouse(mouse_pos)
                    if mouse_pos:
                        print("Received:", mouse_pos)
                        self.waiting_for_msg = False
                except BlockingIOError:
                    pass


