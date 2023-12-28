import pygame
from classes.start_menu import Menu
from classes.board import Board
from classes.checking_for_winner import Graph
import time
import random


class Game:
    def __init__(self, win):
        self.win = win
        self.menu = Menu()
        self.start_menu()
        self.start_game = False
        self.board = Board()
        self.player1_turn = True
        self.game_started = False
        self.game_ended = False
        self.moves = []

    def start_menu(self):
        self.menu.draw_menu(self.win)

    def update_mouse(self, pos):
        # Check if the start button is clicked and initiate the game.
        # It might be a better approach to create a dedicated menu outside of the game class.
        # Consider designing a menu system where the game initializes when the start button is clicked,
        # and add separate buttons for different game modes

        self.start_game = self.menu.start_button.mouse(pos)
        if self.start_game:
            self.menu.start_button.toggle_state()
            self.board.draw_board(self.win)
            pygame.display.flip()
            self.start_game = False
            self.game_started = True
            return False

        self.revert_move(pos)

        if self.game_started and not self.game_ended:

            i, j = self.board.get_hex_cords(pos)
            if i == -1:
                return False
            self.handle_move(i, j)
            return True

    def handle_move(self, i, j):
        self.moves.append((i, j))
        # Update cell color on the current move.
        cell = self.board.hex_cells[i][j]
        cell.used = True
        cell.color, cell.owner = ((255, 255, 0), 'Yellow') if self.player1_turn else ((0, 0, 255), 'Blue')

        # Check for a winner and update the game state.
        graph = Graph(self.board.hex_cells, 1 if self.player1_turn else 2)
        cell.draw(self.win)
        self.player1_turn = not self.player1_turn
        if graph.winner:
            self.game_ended = True
            self.animate_winner(graph)
        pygame.display.flip()

    def revert_move(self, pos):
        if not self.board.back_button.mouse(pos) or not self.moves:
            return False, None
        self.game_ended = False  # I know what I must to add, just remainder
        i, j = self.moves[-1]
        cell = self.board.hex_cells[i][j]
        cell.used, cell.color, cell.owner = False, (255, 255, 255), None

        cell.draw(self.win)
        pygame.display.flip()
        self.player1_turn = not self.player1_turn
        self.moves.pop()
        return True, (i, j)

    def animate_winner(self, graph):
        """Animate the winning path by flashing the cells."""
        for k in range(6):
            color = (0, 255, 0) if k % 2 == 0 else (255, 255, 0) if graph.color == 1 else (0, 0, 255)
            for i, j in graph.wining_cluster:
                cell = self.board.hex_cells[i][j]
                cell.color = color
                cell.draw(self.win)
            pygame.display.flip()
            time.sleep(0.35)


class GameBot(Game):
    def __init__(self, win):
        super().__init__(win)
        self.empty_places = [(row, column) for row in range(11) for column in range(11)]

    def update_mouse(self, pos):
        move_made = super().update_mouse(pos)
        # @TODO add function which chose move for bot
        if move_made and not self.game_ended:
            self.empty_places.remove(self.moves[-1])
            random_element = random.choice(self.empty_places)
            i, j = random_element
            self.handle_move(i, j)
            self.empty_places.remove(random_element)

    def revert_move(self, pos):
        n = 1 if self.game_ended and not self.player1_turn else 2
        for i in range(n):
            result, coordinate = super().revert_move(pos)
            if result:
                self.empty_places.append(coordinate)
