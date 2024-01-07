from classes.console_board import ConsoleBoard
from classes.check_for_win import WinnerChecker
import random


class Game:
    def __init__(self):
        self.board = ConsoleBoard()
        self.player1_turn = True
        self.game_ended = False
        self.moves = []

    def handle_move(self, i, j):
        if self.board.cells[i][j] != 0 or self.game_ended:
            return False
        self.moves.append((i, j))
        # Update cell color on the current move.
        self.board.cells[i][j] = 1 if self.player1_turn else 2

        # Check for a winner and update the game state.
        wins = WinnerChecker(self.board.cells, 1 if self.player1_turn else 2, True)
        self.player1_turn = not self.player1_turn
        if wins.winner:
            self.game_ended = True
        return True

    def revert_move(self):
        if not self.moves:
            return False, None
        # if self.game_ended:
        #     self.board.draw_board(self.win)
        self.game_ended = False
        i, j = self.moves[-1]
        self.board.cells[i][j] = 0
        self.player1_turn = not self.player1_turn
        self.moves.pop()
        return True, (i, j)


class GameBot(Game):
    def __init__(self):
        super().__init__()
        self.empty_places = [(row, column) for row in range(11) for column in range(11)]

    def handle_move(self, i, j):
        move_made = super().handle_move(i, j)
        # @TODO add function which chose move for bot
        if move_made and not self.game_ended:
            self.empty_places.remove(self.moves[-1])
            self.make_random_move()
        return move_made

    def make_random_move(self):
        random_element = random.choice(self.empty_places)
        i, j = random_element
        super().handle_move(i, j)
        self.empty_places.remove(random_element)

    def revert_move(self):
        n = self.how_much_moves_revert()
        for i in range(n):
            result, coordinate = super().revert_move()
            if result:
                self.empty_places.append(coordinate)

    def how_much_moves_revert(self):
        return 1 if self.game_ended and not self.player1_turn else 2


class GameBotFirst(GameBot):
    def __init__(self):
        super().__init__()
        self.make_random_move()

    def how_much_moves_revert(self):
        if len(self.moves) == 1:
            return 0
        elif len(self.moves) == 2:
            return 1
        return 1 if self.game_ended and self.player1_turn else 2
