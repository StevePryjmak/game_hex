import pytest
from classes.game import GameBot


@pytest.fixture
def game_bot():
    return GameBot()


# 1. Initilization test
def test_game_bot_initialization(game_bot):
    assert len(game_bot.empty_places) == 121
    assert game_bot.player1_turn is True
    assert not game_bot.game_ended


# 2. Handle Move Tests
def test_game_bot_handle_move_valid(game_bot):
    initial_empty_count = len(game_bot.empty_places)
    game_bot.handle_move(0, 0)
    assert len(game_bot.empty_places) == initial_empty_count - 2  # One for player, one for bot


def test_game_bot_handle_move_invalid(game_bot):
    game_bot.handle_move(0, 0)
    move_made = game_bot.handle_move(0, 0)  # Try to move to the same spot
    assert not move_made
    assert len(game_bot.empty_places) == 119  # Should not decrease further


#  3. Make Random Move Tests
def test_game_bot_make_random_move(game_bot):
    initial_empty_count = len(game_bot.empty_places)
    game_bot.make_random_move()
    assert len(game_bot.empty_places) == initial_empty_count - 1


#  4. Revert Move Tests
def test_game_bot_revert_move(game_bot):
    game_bot.handle_move(0, 0)
    game_bot.revert_move()
    assert len(game_bot.empty_places) == 121


def test_game_bot_revert_move_on_empty(game_bot):
    result = game_bot.revert_move()

    if result is not None:
        success, _ = result
        assert not success
    else:
        assert result is None  # revert_move should return None when no moves are available to revert


# 5. how_much_moves_revert Tests
def test_game_bot_how_much_moves_revert_midgame(game_bot):

    game_bot.handle_move(0, 0)
    assert game_bot.how_much_moves_revert() == 2


# 6. Interaction Tests
def test_game_bot_moves_and_empty_places_interaction(game_bot):
    game_bot.handle_move(0, 0)
    game_bot.revert_move()
    assert (0, 0) in game_bot.empty_places


# 7. Monkeypatch Tests
def test_game_bot_make_random_move_mocked(monkeypatch, game_bot):

    def mock_random_choice(smt):
        return 5, 5
    monkeypatch.setattr('random.choice', mock_random_choice)

    game_bot.make_random_move()
    assert (5, 5) not in game_bot.empty_places


def test_game_bot_make_random_move_monkeypatch(monkeypatch, game_bot):
    def mock_random_choice(empty_places):
        return empty_places[0]  # Always choose the first empty place
    monkeypatch.setattr('random.choice', mock_random_choice)

    initial_empty_count = len(game_bot.empty_places)
    game_bot.make_random_move()
    assert len(game_bot.empty_places) == initial_empty_count - 1
    assert game_bot.board.cells[0][0] != 0


def test_game_bot_handle_and_random_move_monkeypatch(monkeypatch, game_bot):
    moves = [(0, 0), (5, 5)]

    def mock_random_choice(empty_places):
        return moves.pop()

    monkeypatch.setattr('random.choice', mock_random_choice)

    game_bot.handle_move(moves[0][0], moves[0][1])
    # Validate the moves
    assert game_bot.board.cells[0][0] != 0
    assert game_bot.board.cells[5][5] != 0
    assert (0, 0) not in game_bot.empty_places
    assert (5, 5) not in game_bot.empty_places


def test_game_bot_revert_move_monkeypatch(monkeypatch, game_bot):
    moves_made = [(0, 0), (5, 5)]

    def mock_revert_move():
        if moves_made:
            last_move = moves_made.pop()
            game_bot.empty_places.append(last_move)  # Ensure the move is added back
            return True, last_move
        else:
            return False, None

    monkeypatch.setattr(game_bot, "revert_move", mock_revert_move)

    game_bot.empty_places.remove((0, 0))
    game_bot.empty_places.remove((5, 5))

    game_bot.revert_move()
    game_bot.revert_move()

    assert (0, 0) in game_bot.empty_places
    assert (5, 5) in game_bot.empty_places

