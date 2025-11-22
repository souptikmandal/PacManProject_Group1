import pytest
import pygame
from game_board import GameBoard


@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def game_board():
    return GameBoard()


def test_gameboard_initialization(game_board):
    assert game_board.width == 800
    assert game_board.height == 600
    assert isinstance(game_board.walls, list)
    assert isinstance(game_board.pellets, list)
    assert isinstance(game_board.power_pellets, list)
    assert len(game_board.walls) > 0
    assert len(game_board.pellets) > 0
    assert len(game_board.power_pellets) > 0


def test_outer_walls_dimensions(game_board):
    """Ensure the four outer walls exist and have correct placement."""
    walls = game_board.walls[:4]
    top, left, bottom, right = walls

    # Check top wall
    assert top.topleft == (0, 0)
    assert top.width == game_board.width
    assert top.height == 20

    # Check left wall
    assert left.topleft == (0, 0)
    assert left.height == game_board.height
    assert left.width == 20

    # Check bottom wall
    assert bottom.bottomleft == (0, game_board.height)
    assert bottom.height == 20

    # Check right wall
    assert right.topright == (game_board.width, 0)
    assert right.width == 20


def test_pellets_do_not_overlap_walls(game_board):
    """Ensure no pellet was placed inside a wall."""
    for pellet in game_board.pellets:
        pellet_pos = (pellet.x, pellet.y)
        for wall in game_board.walls:
            assert not wall.collidepoint(
                pellet_pos
            ), f"Pellet at {pellet_pos} overlaps with wall at {wall}"


def test_power_pellet_positions(game_board):
    """Verify that power pellets are at expected coordinates."""
    expected_positions = [
        (game_board.width - 50, 50),
        (50, game_board.height - 50),
        (game_board.width - 50, game_board.height - 50),
    ]

    actual_positions = [(pp.x, pp.y) for pp in game_board.power_pellets]
    for pos in expected_positions:
        assert pos in actual_positions, f"Expected power pellet at {pos}"
