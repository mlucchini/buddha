from buddha.platform.position import Position
from buddha.platform.vector import Vector


def assert_eq(left, right):
    assert left == right, "{} != {}".format(left, right)


def test_normalize_constraints():
    expected = Position(Vector(-1.0, -1.0, -1.0), Vector(1.0, 1.0, 1.0))
    normalized = Position(Vector(-2.0, -10.0, -1.0), Vector(1.0, 2.0, 15.0))\
        .normalize_with(Position(Vector(-1.0, -1.0, -1.0), Vector(-1.0, -1.0, -1.0)),
                        Position(Vector(1.0, 1.0, 1.0), Vector(1.0, 1.0, 1.0)))

    assert_eq(normalized, expected)


def test_normalize_range():
    expected = Position(Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0))
    normalized = Position(Vector(-2.0, -10.0, -10.0), Vector(1.0, 2.0, 15.0))\
        .normalize_with(Position(Vector(-4.0, -20.0, -15.0), Vector(0.0, -2.0, 14.0)),
                        Position(Vector(0.0, 0.0, -5.0), Vector(2.0, 6.0, 16.0)))

    assert_eq(normalized, expected)
