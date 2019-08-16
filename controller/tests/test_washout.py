from buddha.platform.position import Position
from buddha.platform.vector import Vector
from buddha.washout.filters.rotation_high_pass_filter import RotationHighPassFilter
from buddha.washout.filters.translation_high_pass_filter import TranslationHighPassFilter
from buddha.washout.filters.translation_low_pass_filter import TranslationLowPassFilter
from buddha.washout.motion import Motion
from buddha.washout.washout_filter import WashoutFilter

EPSILON = 0.01

def assert_eq(left, right):
    assert abs(left - right) < EPSILON, "{} != {}".format(left, right)

def assert_position_eq(left, right):
    assert_eq(left.translation.x, right.translation.x)
    assert_eq(left.translation.y, right.translation.y)
    assert_eq(left.translation.z, right.translation.z)
    assert_eq(left.rotation.x, right.rotation.x)
    assert_eq(left.rotation.y, right.rotation.y)
    assert_eq(left.rotation.z, right.rotation.z)

def make_washout_filter():
    sampling_interval = 10.0
    cutoff_frequency_high_pass = 2.5
    cutoff_frequency_low_pass = 5
    damping_ratio = 1.0

    translation_high_pass_filters = [TranslationHighPassFilter(sampling_interval, cutoff_frequency_high_pass),
                                     TranslationHighPassFilter(sampling_interval, cutoff_frequency_high_pass),
                                     TranslationHighPassFilter(sampling_interval, cutoff_frequency_high_pass)]

    translation_low_pass_filters = [TranslationLowPassFilter(sampling_interval, cutoff_frequency_low_pass, damping_ratio),
                                    TranslationLowPassFilter(sampling_interval, cutoff_frequency_low_pass, damping_ratio)]

    rotation_high_pass_filters = [RotationHighPassFilter(sampling_interval, cutoff_frequency_high_pass),
                                  RotationHighPassFilter(sampling_interval, cutoff_frequency_high_pass),
                                  RotationHighPassFilter(sampling_interval, cutoff_frequency_high_pass)]

    return WashoutFilter(translation_high_pass_filters, translation_low_pass_filters, rotation_high_pass_filters, sampling_interval)

def test_translation_high_pass_filter():
    f = TranslationHighPassFilter(10.0, 5.0)

    assert_eq(f.apply(5.0), 4.76)
    assert_eq(f.apply(7.0), 6.20)
    assert_eq(f.apply(9.0), 7.48)
    assert_eq(f.apply(0.0), -1.84)
    assert_eq(f.apply(0.0), -1.70)

def test_translation_low_pass_filter():
    f = TranslationLowPassFilter(10.0, 5.0, 1.0)

    assert_eq(f.apply(5.0), 0.0)
    assert_eq(f.apply(7.0), 0.02)
    assert_eq(f.apply(9.0), 0.04)
    assert_eq(f.apply(0.0), 0.08)
    assert_eq(f.apply(0.0), 0.13)

def test_rotation_high_pass_filter():
    f = RotationHighPassFilter(10.0, 5.0)

    assert_eq(f.apply(5.0), 4.88)
    assert_eq(f.apply(7.0), 6.59)
    assert_eq(f.apply(9.0), 8.22)
    assert_eq(f.apply(0.0), -0.96)
    assert_eq(f.apply(0.0), -0.91)

def test_simple_washout():
    expected_position = Position(Vector(0.0, 0.0, -0.96), Vector(0.0, 0.0, 0.0))

    washout_filter = make_washout_filter()
    position = washout_filter.apply(Motion(Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0)))

    assert_position_eq(position, expected_position)

def test_multiple_apply_washout():
    expected_positions = [Position(Vector(0.0, 0.0, -0.96), Vector(0.03, 0.04, 0.05)),
                          Position(Vector(-0.03, 0.02, -1.87), Vector(0.06, 0.08, 0.09)),
                          Position(Vector(-0.15, 0.11, -2.73), Vector(0.08, 0.11, 0.14)),
                          Position(Vector(-0.36, 0.27, -3.57), Vector(0.11, 0.15, 0.19)),]

    washout_filter = make_washout_filter()

    for i in range(4):
        position = washout_filter.apply(Motion(Vector(1.0, 2.0, 3.0), Vector(3.0, 4.0, 5.0)))
        assert_position_eq(position, expected_positions[i])
