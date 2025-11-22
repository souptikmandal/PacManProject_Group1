import pytest
import pygame
from pac_man import Pac_Man


@pytest.fixture
def pac_man():
    return Pac_Man(100, 100)


@pytest.fixture
def walls():
    return [
        pygame.Rect(0, 0, 20, 600),  # Left wall
        pygame.Rect(200, 200, 20, 20),  # Small obstacle
        pygame.Rect(780, 0, 20, 600),  # Right wall
    ]


def test_pac_man_initialization(pac_man):
    assert pac_man.x == 100
    assert pac_man.y == 100
    assert pac_man.direction == "right"
    assert pac_man.speed == 2
    assert pac_man.radius == 10


def test_pac_man_movement_no_walls(pac_man):
    initial_x = pac_man.x
    initial_y = pac_man.y

    pac_man.move("right", [])
    assert pac_man.x == initial_x + pac_man.speed
    assert pac_man.y == initial_y
    assert pac_man.direction == "right"

    pac_man.move("left", [])
    assert pac_man.x == initial_x
    assert pac_man.y == initial_y
    assert pac_man.direction == "left"


def test_pac_man_wall_collision(pac_man, walls):
    # Move towards left wall
    pac_man.x = 25
    pac_man.y = 100
    pac_man.move("left", walls)
    assert pac_man.x == 25  # Should not move through wall

    # Move towards obstacle
    pac_man.x = 190
    pac_man.y = 210
    pac_man.move("right", walls)
    assert pac_man.x == 190  # Should not move through obstacle


def test_pac_man_movement_with_obstacles(pac_man, walls):
    # Step 1: Move pac_man towards an obstacle (left wall)
    pac_man.x = 25
    pac_man.y = 100
    pac_man.move("left", walls)
    assert pac_man.x == 25  # Should not move through the left wall

    # Step 2: Move pac_man towards an obstacle (small obstacle at (200, 200))
    pac_man.x = 190
    pac_man.y = 210
    pac_man.move("right", walls)
    assert pac_man.x == 190  # Should not move through the small obstacle

    # Step 3: Move pac_man towards the right wall (new right wall at x=780)
    pac_man.x = 780
    pac_man.y = 100
    pac_man.move("right", walls)
    # Assert that the pac_man's position hasn't changed, as they can't move past the wall
    assert pac_man.x == 780  # Should not move beyond the right wall
