import math
import random
import timeit

from buddha.platform.platform import Platform
from buddha.platform.position import Position
from buddha.platform.vector import Vector

EPSILON = 0.01


def assert_angle_eq(angle, expected):
    for i in range(6):
        assert abs(angle[i] - expected[i]) < EPSILON, "{} != {}".format(angle[i], expected[i])


def make_and_transform_platform(position):
    platform = Platform(base_angles=[74.9, 105.1, 194.9, 225.1, 314.9, 345.1],
                        platform_angles=[82.9, 97.1, 202.9, 217.1, 322.9, 337.1],
                        beta=[0, 180, 120, 300, 240, 60],
                        initial_height=320.0, base_radius=150.0, platform_radius=110.0, horn_length=100.0,
                        leg_length=330.0, max_translation=50.0, max_rotation=math.pi / 4)
    return platform.update(position)


def make_and_transform_platform_randomly_n_times(n):
    platform = Platform()
    for i in range(n):
        position = Position(Vector(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)), Vector(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)))
        platform.update(position)


def test_initial_position():
    angle = make_and_transform_platform(Position(Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0)))
    assert_angle_eq(angle, [-99.40, 99.40, -99.40, 99.40, -99.40, 99.40])


def test_translate_x():
    angle = make_and_transform_platform(Position(Vector(1.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0)))
    assert_angle_eq(angle, [-90.42, 112.43, -109.89, 98.83, -104.37, 93.27])


def test_translate_x_y_z():
    angle = make_and_transform_platform(Position(Vector(1.0, 1.0, 1.0), Vector(0.0, 0.0, 0.0)))
    assert_angle_eq(angle, [-117.76, 137.07, -132.42, 139.64, -142.31, 115.99])


def test_rotate_x():
    angle = make_and_transform_platform(Position(Vector(0.0, 0.0, 0.0), Vector(1.0, 0.0, 0.0)))
    assert_angle_eq(angle, [-147.28, 147.28, -79.95, 77.06, -77.06, 79.95])


def test_rotate_x_y_z():
    angle = make_and_transform_platform(Position(Vector(0.0, 0.0, 0.0), Vector(1.0, 1.0, 1.0)))
    assert_angle_eq(angle, [-129.18, 135.36, -145.60, 108.48, -50.82, 35.269])


def test_translate_x_y_z_rotate_x_y_z():
    angle = make_and_transform_platform(Position(Vector(0.5, 0.5, 0.5), Vector(0.5, 0.5, 0.5)))
    assert_angle_eq(angle, [-130.56, 137.76, -136.47, 118.27, -102.57, 72.39])


def test_translate_x_y_z_rotate_x_y_z_with_various_values():
    angle = make_and_transform_platform(Position(Vector(-0.3, -0.15, 0.05), Vector(-0.54, -0.19, 0.48)))
    assert_angle_eq(angle, [-91.91, 66.61, -110.19, 101.95, -129.76, 116.08])


def test_handle_nans():
    angle = make_and_transform_platform(Position(Vector(-1.0, -1.0, -1.0), Vector(1.0, 1.0, 1.0)))
    assert_angle_eq(angle, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])


def test_performance():
    total = timeit.timeit("make_and_transform_platform_randomly_n_times(1000)", number=1, globals=globals())
    assert total / 1000 < 0.0002
