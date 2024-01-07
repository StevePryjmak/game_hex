import pytest
import random
from classes.game import Game
from classes.console_board import ConsoleBoard
from classes.check_for_win import WinnerChecker


@pytest.fixture
def game():
    return Game()


@pytest.fixture
def console_board():
    return ConsoleBoard()


def test_console_board_init(console_board):
    assert len(console_board.cells) == 11
    for row in console_board.cells:
        assert len(row) == 11
        assert all(cell == 0 for cell in row)


def test_console_board_update(console_board):
    console_board.cells[5][5] = 1  # Update a cell
    assert console_board.cells[5][5] == 1


class MockBoard:
    def __init__(self):
        self.cells = [[0] * 3 for _ in range(3)]


def test_init(game, monkeypatch):
    monkeypatch.setattr(game, "board", MockBoard())
    assert game.player1_turn is True
    assert game.game_ended is False
    assert game.moves == []

    assert game.board.cells == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    patched_board = MockBoard()
    patched_board.cells = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert game.board.cells == patched_board.cells


def test_game_init(game):
    assert game.player1_turn is True
    assert game.game_ended is False
    assert game.moves == []
    assert len(game.board.cells) == 11
    for row in game.board.cells:
        assert len(row) == 11
        assert all(cell == 0 for cell in row)


def test_game_end_condition(game):
    for j in range(11):  # Assuming a win is a complete row
        game.handle_move(10, j)
        game.handle_move(0, j)
    assert game.game_ended is True


def test_game_alternate_turns(game):
    game.handle_move(0, 0)
    assert game.player1_turn is False
    game.handle_move(1, 0)
    assert game.player1_turn is True


def test_handle_move_valid(game):
    assert game.handle_move(0, 0) is True
    assert game.board.cells[0][0] == 1
    assert game.moves == [(0, 0)]


def test_handle_move_invalid(game):
    game.handle_move(0, 0)  # First move is valid
    assert game.handle_move(0, 0) is False  # Can't move to same place


def test_revert_move(game):
    game.handle_move(0, 0)
    success, last_move = game.revert_move()
    assert success is True
    assert last_move == (0, 0)
    assert game.board.cells[0][0] == 0
    assert game.moves == []


def test_game_revert_at_end(game):
    for j in range(11):
        game.handle_move(5, j)
        game.handle_move(0, j)
    assert game.game_ended is True
    game.revert_move()
    assert game.player1_turn is False


def test_revert_move_empty(game):
    success, last_move = game.revert_move()
    assert success is False
    assert last_move is None


@pytest.fixture
def winner_checker():
    # A winner checker for player 1 (color = 1) and console mode is true
    board = ConsoleBoard()
    return WinnerChecker(board.cells, 1, True)


def test_winner_checker_initialization(winner_checker):
    assert winner_checker.color == 1
    assert not winner_checker.winner
    assert len(winner_checker.check_positions) == 11
    assert len(winner_checker.end_positions) == 11


def test_winner_checker_no_winner(game):
    # Making 20 random moves on the board there should be no winner
    for _ in range(20):
        row = random.randint(0, 10)
        col = random.randint(0, 10)
        game.handle_move(row, col)
    winner_checker = WinnerChecker(game.board.cells, 1, True)
    # Check if the winner_checker's winner attribute is set to False after random moves
    assert not winner_checker.winner


def test_winner_checker_winner(game):
    # Fill all board and there should be winner
    empty_places = [(row, column) for row in range(11) for column in range(11)]
    for i, j in empty_places:
        game.handle_move(i, j)
    winner_checker_first = WinnerChecker(game.board.cells, 1, True)
    winner_checker_second = WinnerChecker(game.board.cells, 2, True)
    assert winner_checker_first.winner
    assert not winner_checker_second.winner
    assert winner_checker_first.winner or winner_checker_second.winner


def test_winner_checker_potential_winner_scenario(game):
    # Manually setting up a winning scenario for player 2
    for j in range(11):
        game.handle_move(5, j)
        game.handle_move(0, j)
        # Filling an entire row with player 1's pieces and another row with second player
    winner_checker_first = WinnerChecker(game.board.cells, 1, True)
    winner_checker_second = WinnerChecker(game.board.cells, 2, True)
    assert not winner_checker_first.winner
    assert winner_checker_second.winner


def test_winner_checker_diagonal_condition(game):
    for i in range(11):
        game.board.cells[i][i] = 1  # Diagonal fill for player 1
    winner_checker = WinnerChecker(game.board.cells, 1, True)
    assert not winner_checker.winner


def test_winner_checker_half_bord(game):
    for i in range(11):
        for j in range(11):
            if j > i:
                game.board.cells[i][j] = 1
            elif j < i:
                game.board.cells[i][j] = 2
    winner_checker1 = WinnerChecker(game.board.cells, 1, True)
    winner_checker2 = WinnerChecker(game.board.cells, 2, True)
    assert not (winner_checker1.winner or winner_checker2.winner)


def test_winner_checker_half_bord_is_winner(game):
    for i in range(11):
        for j in range(11):
            if j > i:
                game.board.cells[i][j] = 1
            else:
                game.board.cells[i][j] = 2
    winner_checker2 = WinnerChecker(game.board.cells, 2, True)
    assert winner_checker2.winner


def test_winner_checker_get_neighbors(winner_checker):
    winner_checker.board[1][1] = 1
    winner_checker.board[1][2] = 1
    winner_checker.board[1][0] = 1
    _, neighbors, _ = winner_checker.get_neighbors(1, 1, 1, [])
    assert set(neighbors) == {(1, 0), (1, 2)}


def test_winner_checker_no_neighbors(winner_checker):
    # Testing with no neighbors
    _, neighbors, _ = winner_checker.get_neighbors(5, 5, 1, [])
    assert neighbors == []
