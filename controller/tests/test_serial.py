from __future__ import print_function, division, absolute_import

from tempfile import TemporaryFile

from buddha.serial.serial import Order, write_order, read_order, write_i16, write_i32, read_i16, read_i32


def assert_eq(left, right):
    assert left == right, "{} != {}".format(left, right)


def test_read_write_orders():
    servo_angle = 512  # 2^9
    big_number = -32768  # -2^15

    f = TemporaryFile()

    write_order(f, Order.SET_SERVO_ANGLE)
    write_i16(f, servo_angle)

    write_order(f, Order.ERROR)
    write_i32(f, big_number)

    f.seek(0, 0)

    read_2nd_order = read_order(f)
    read_servo_angle = read_i16(f)

    read_3rd_order = read_order(f)
    read_big_number = read_i32(f)

    assert_eq(read_2nd_order, Order.SET_SERVO_ANGLE)
    assert_eq(read_servo_angle, servo_angle)

    assert_eq(read_3rd_order, Order.ERROR)
    assert_eq(read_big_number, big_number)
