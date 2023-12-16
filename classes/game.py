import pygame
from .start_menu import Menu
from .board import Board
from .checking_for_winner import Graph


class Game:
    def __init__(self, win):
        self.win = win
        self.menu = Menu()
        self.start_menu()
        self.start_game = False
        self.board = Board()
        self.move = True
        self.game_started = False

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

        if self.game_started:
            for i in range(0, 11):
                for j in range(0, 11):
                    if self.board.hex_cells[i][j].clicked(pos):
                        if self.move:
                            self.board.hex_cells[i][j].color = (0, 255, 0)
                            self.board.hex_cells[i][j].occupated_by = 'Green'
                            graph = Graph(self.board.hex_cells, 1)
                            self.board.hex_cells[i][j].draw(self.win)
                            self.move = not self.move
                        elif not self.move:
                            self.board.hex_cells[i][j].color = (0, 0, 255)
                            self.board.hex_cells[i][j].occupated_by = 'Blue'
                            graph = Graph(self.board.hex_cells, 2)
                            self.board.hex_cells[i][j].draw(self.win)
                            self.move = not self.move

            pygame.display.flip()