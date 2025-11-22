import pytest
import pygame
from item import Pellet, PowerPellet


@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def surface():
    # Minimal surface for draw calls
    return pygame.Surface((100, 100))


def test_pellet_initialization():
    p = Pellet(10, 20)
    assert hasattr(p, "x")
    assert p.x == 10
    # y should be present and equal to constructor argument
    assert hasattr(p, "y"), "Pellet should store the 'y' coordinate"
    assert getattr(p, "y") == 20
    # radius should be small pellet size
    assert hasattr(p, "radius")
    assert p.radius == 2
    # collected flag should exist and default to False
    assert hasattr(p, "collected"), "Pellet should track whether it's collected"
    assert getattr(p, "collected") is False


def test_pellet_draw_respects_collected_flag(surface, monkeypatch):
    p = Pellet(30, 40)
    # Ensure expected attributes exist
    assert hasattr(p, "collected")
    assert hasattr(p, "y")

    calls = {"count": 0}

    def fake_circle(screen, color, pos, radius):
        calls["count"] += 1

    monkeypatch.setattr(pygame.draw, "circle", fake_circle)

    # When not collected, draw should call pygame.draw.circle exactly once
    p.collected = False
    p.draw(surface)
    assert calls["count"] == 1

    # When collected, it should not draw
    p.collected = True
    p.draw(surface)
    assert calls["count"] == 1  # unchanged


def test_power_pellet_initialization():
    pp = PowerPellet(50, 60)
    assert pp.x == 50
    assert pp.y == 60
    assert pp.radius == 8
    assert pp.collected is False


def test_power_pellet_draw_respects_collected_flag(surface, monkeypatch):
    pp = PowerPellet(70, 80)

    calls = {"count": 0}

    def fake_circle(screen, color, pos, radius):
        calls["count"] += 1

    monkeypatch.setattr(pygame.draw, "circle", fake_circle)

    # Not collected -> draws
    pp.collected = False
    pp.draw(surface)
    assert calls["count"] == 1

    # Collected -> no further draws
    pp.collected = True
    pp.draw(surface)
    assert calls["count"] == 1
