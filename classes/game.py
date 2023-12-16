import pygame
from .start_menu import Menu
from .board import Board
from .checking_for_winner import Graph
from itertools import product
import time

class Game:
    def __init__(self, win):
        self.win = win
        self.menu = Menu()
        self.start_menu()
        self.start_game = False
        self.board = Board()
        self.move = True
        self.game_started = False
        self.game_ended = False

    def start_menu(self):
        self.menu.draw_menu(self.win)

    def update_mouse(self, pos):
        self.start_game = self.menu.start_button.mouse(pos)
        if self.start_game:
            self.win.fill((0, 0, 0))
            self.board.draw_board(self.win)
            pygame.display.flip()
            self.start_game = False
            self.game_started = True
            return 0

        if self.game_started and not self.game_ended:
            for i, j in product(range(0, 11), repeat=2):

                if self.board.hex_cells[i][j].clicked(pos):
                    cell = self.board.hex_cells[i][j]
                    if self.move:
                        cell.color = (255, 255, 0)
                        cell.occupated_by = 'Yellow'
                    elif not self.move:
                        cell.color = (0, 0, 255)
                        cell.occupated_by = 'Blue'
                    graph = Graph(self.board.hex_cells, 1 if self.move else 2)
                    cell.draw(self.win)
                    self.move = not self.move
                    if graph.winner:
                        self.game_ended = True
                        for k in range(0, 10):
                            color = (255, 255, 255) if k % 2 == 0 else (255, 255, 0) if graph.color == 1 else (0, 0, 255)
                            for i, j in graph.wining_cluster:
                                cell = self.board.hex_cells[i][j]
                                cell.color = color
                                cell.draw(self.win)
                            pygame.display.flip()
                            time.sleep(0.25)

                    break

            pygame.display.flip()