import pygame
from classes.start_menu import Menu, GameEndMenu
from classes.board import Board
from classes.checking_for_winner import Graph
import time
from classes.button import Button
import random
from classes.constants import FIRST_PLAYER_COLOR, SECOND_PLAYER_COLOR


class GameParent:
    def __init__(self, win):
        self.win = win
        self.game_ended = False

class Game:
    def __init__(self, win):
        self.win = win
        self.board = Board(self.revert_move)
        self.player1_turn = True
        self.game_ended = False
        self.moves = []
        self.start_game()

    def start_game(self):
        self.board.draw_board(self.win)

    def update_mouse(self, pos):
        self.revert_move(pos)

        if not self.game_ended:

            i, j = self.board.get_hex_cords(pos)
            if i == -1 or self.board.hex_cells[i][j].used:
                return False
            self.handle_move(i, j)
            return True

    def handle_move(self, i, j):
        self.moves.append((i, j))
        # Update cell color on the current move.
        cell = self.board.hex_cells[i][j]
        cell.used = True
        cell.color, cell.owner = FIRST_PLAYER_COLOR if self.player1_turn else SECOND_PLAYER_COLOR

        # Check for a winner and update the game state.
        graph = Graph(self.board.hex_cells, 1 if self.player1_turn else 2)
        cell.draw(self.win)
        self.player1_turn = not self.player1_turn
        if graph.winner:
            self.game_ended = True
        pygame.display.flip()

    def revert_move(self, pos):
        if not self.board.back_button.rect.collidepoint(pos) or not self.moves:
            return False, None
        if self.game_ended:
            self.board.draw_board(self.win)
        self.game_ended = False
        i, j = self.moves[-1]
        cell = self.board.hex_cells[i][j]
        cell.used, cell.color, cell.owner = False, (255, 255, 255), None

        cell.draw(self.win)
        pygame.display.flip()
        self.player1_turn = not self.player1_turn
        self.moves.pop()
        return True, (i, j)

    def animate_winner(self, graph, color):
        """Animate the winning path by flashing the cells."""
        for i, j in graph.wining_cluster:
            cell = self.board.hex_cells[i][j]
            cell.color = color
            cell.draw(self.win)


class GameBot(Game):
    def __init__(self, win):
        super().__init__(win)
        self.empty_places = [(row, column) for row in range(11) for column in range(11)]

    def update_mouse(self, pos):
        move_made = super().update_mouse(pos)
        # @TODO add function which chose move for bot
        if move_made and not self.game_ended:
            self.empty_places.remove(self.moves[-1])
            self.make_random_move()

    def make_random_move(self):
        random_element = random.choice(self.empty_places)
        i, j = random_element
        self.handle_move(i, j)
        self.empty_places.remove(random_element)

    def revert_move(self, pos):
        n = self.how_much_moves_revert()
        for i in range(n):
            result, coordinate = super().revert_move(pos)
            if result:
                self.empty_places.append(coordinate)

    def how_much_moves_revert(self):
        return 1 if self.game_ended and not self.player1_turn else 2


class GameBotFirst(GameBot):
    def __init__(self, win):
        super().__init__(win)
        self.make_random_move()

    def how_much_moves_revert(self):
        if len(self.moves) == 1:
            return 0
        elif len(self.moves) == 2:
            return 1
        return 1 if self.game_ended and self.player1_turn else 2
