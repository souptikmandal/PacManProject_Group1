import pytest
import pygame
from game_board import GameBoard
from ghost import Ghost
from player import Player


@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


def test_ghosts_not_spawned_in_walls():
    """Ensure ghosts initialized at typical spawn positions are not inside walls."""

    game_board = GameBoard()

    spawn_positions = [
        (100, 100),
        (game_board.width - 100, 100),
        (100, game_board.height - 100),
        (game_board.width - 100, game_board.height - 100),
    ]

    ghosts = [Ghost(x, y, (255, 0, 0)) for x, y in spawn_positions]

    for ghost in ghosts:
        ghost_rect = pygame.Rect(
            ghost.x - ghost.radius,
            ghost.y - ghost.radius,
            ghost.radius * 2,
            ghost.radius * 2,
        )
        for wall in game_board.walls:
            assert not ghost_rect.colliderect(wall), (
                f"Ghost at ({ghost.x}, {ghost.y}) spawns inside wall {wall}"
            )


def test_ghost_initialization():
    """Test that a ghost is initialized with correct properties."""
    ghost = Ghost(100, 150, (255, 0, 0))

    assert ghost.x == 100
    assert ghost.y == 150
    assert ghost.color == (255, 0, 0)
    assert ghost.speed == 1
    assert ghost.radius == 10
    assert ghost.direction in ["right", "left", "up", "down"]
    assert ghost.scared == False
    assert ghost.scared_timer == 0


def test_ghost_movement_without_walls():
    """Test that ghost moves in the correct direction when there are no walls."""
    ghost = Ghost(200, 200, (255, 0, 0))
    player = Player(300, 200)

    # Set a specific direction
    ghost.direction = "right"
    initial_x = ghost.x

    # Move the ghost with no walls
    ghost.move([], player)

    # Ghost should have moved right
    assert ghost.x >= initial_x


def test_ghost_scared_mode():
    """Test that ghost scared mode works correctly."""
    ghost = Ghost(200, 200, (255, 0, 0))
    player = Player(300, 200)

    # Enable scared mode
    ghost.scared = True
    ghost.scared_timer = 100

    assert ghost.scared == True
    assert ghost.scared_timer == 100

    # Move ghost once
    ghost.move([], player)

    # Timer should decrease
    assert ghost.scared_timer == 99


def test_ghost_scared_mode_expires():
    """Test that ghost scared mode expires after timer runs out."""
    ghost = Ghost(200, 200, (255, 0, 0))
    player = Player(300, 200)

    # Enable scared mode with short timer
    ghost.scared = True
    ghost.scared_timer = 1

    # Move ghost once
    ghost.move([], player)

    # Scared mode should be disabled
    assert ghost.scared == False
    assert ghost.scared_timer == 0


def test_ghost_collision_with_walls():
    """Test that ghost cannot move through walls."""
    game_board = GameBoard()
    ghost = Ghost(100, 100, (255, 0, 0))
    player = Player(300, 300)

    # Try to move ghost multiple times
    for _ in range(10):
        ghost.move(game_board.walls, player)

    # Ghost should not be stuck in a wall
    ghost_rect = pygame.Rect(
        ghost.x - ghost.radius,
        ghost.y - ghost.radius,
        ghost.radius * 2,
        ghost.radius * 2,
    )

    for wall in game_board.walls:
        assert not ghost_rect.colliderect(wall), (
            f"Ghost at ({ghost.x}, {ghost.y}) moved into wall {wall}"
        )


def test_ghost_chases_player():
    """Test that ghost moves toward player when not scared."""
    ghost = Ghost(100, 100, (255, 0, 0))
    player = Player(500, 100)

    # Ghost is not scared
    ghost.scared = False

    initial_x = ghost.x

    # Move ghost multiple times toward player
    for _ in range(50):
        ghost.move([], player)

    # Ghost should have moved toward player (to the right)
    assert ghost.x > initial_x


def test_ghost_multiple_colors():
    """Test that ghosts can be created with different colors."""
    ghost1 = Ghost(100, 100, (255, 0, 0))  # Red
    ghost2 = Ghost(200, 200, (0, 255, 0))  # Green
    ghost3 = Ghost(300, 300, (255, 0, 255))  # Purple

    assert ghost1.color == (255, 0, 0)
    assert ghost2.color == (0, 255, 0)
    assert ghost3.color == (255, 0, 255)


def test_ghost_speed():
    """Test that ghost moves at the correct speed."""
    ghost = Ghost(200, 200, (255, 0, 0))
    player = Player(300, 200)

    ghost.direction = "right"
    initial_x = ghost.x

    ghost.move([], player)

    # Ghost should move exactly 'speed' pixels
    assert ghost.x == initial_x + ghost.speed
