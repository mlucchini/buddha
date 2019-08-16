from __future__ import print_function, division, unicode_literals, absolute_import

import struct

from enum import Enum


class Order(Enum):
    """
    Pre-defined orders
    """

    HELLO = 10
    CONNECTED = 11
    RECEIVED = 12
    ERROR = 13

    GET_IDENTIFIER = 20
    SET_IDENTIFIER = 21

    GET_SERVO_ANGLE = 30
    SET_SERVO_ANGLE = 31

    GET_MIN_PWM = 40
    SET_MIN_PWM = 41
    GET_MAX_PWM = 42
    SET_MAX_PWM = 43

    GET_ZERO_RAW_POSITION = 50
    SET_ZERO_RAW_POSITION = 51

    GET_GRAVITY_FEED_FORWARD = 60
    SET_GRAVITY_FEED_FORWARD = 61


def read_order(f):
    """
    :param f: file handler or serial file
    :return: (Order Enum Object)
    """
    return Order(read_i8(f))


def read_i8(f):
    """
    :param f: file handler or serial file
    :return: (int8_t)
    """
    return struct.unpack('<b', bytearray(f.read(1)))[0]


def read_i16(f):
    """
    :param f: file handler or serial file
    :return: (int16_t)
    """
    return struct.unpack('<h', bytearray(f.read(2)))[0]


def read_i32(f):
    """
    :param f: file handler or serial file
    :return: (int32_t)
    """
    return struct.unpack('<l', bytearray(f.read(4)))[0]


def write_i8(f, value):
    """
    :param f: file handler or serial file
    :param value: (int8_t)
    """
    if -128 <= value <= 127:
        f.write(struct.pack('<b', value))
    else:
        print("Value error:{}".format(value))


def write_order(f, order):
    """
    :param f: file handler or serial file
    :param order: (Order Enum Object)
    """
    write_i8(f, order.value)


def write_i16(f, value):
    """
    :param f: file handler or serial file
    :param value: (int16_t)
    """
    f.write(struct.pack('<h', value))


def write_i32(f, value):
    """
    :param f: file handler or serial file
    :param value: (int32_t)
    """
    f.write(struct.pack('<l', value))


def decode_order(f, byte, debug=False):
    """
    :param f: file handler or serial file
    :param byte: (int8_t)
    :param debug: (bool) whether to print or not received messages
    """
    try:
        order = Order(byte)
        if order == Order.HELLO:
            msg = "HELLO"
        elif order == Order.GET_SERVO_ANGLE:
            angle = read_i16(f)
            msg = "GET_SERVO_ANGLE {}".format(angle)
        elif order == Order.SET_SERVO_ANGLE:
            msg = "SET_SERVO_ANGLE"
        elif order == Order.CONNECTED:
            msg = "CONNECTED"
        elif order == Order.ERROR:
            msg = "ERROR"
        elif order == Order.RECEIVED:
            msg = "RECEIVED"
        elif order == Order.STOP:
            msg = "STOP"
        elif order == Order.GET_IDENTIFIER:
            identifier = read_i8(f)
            msg = "GET_IDENTIFIER {}".format(identifier)
        elif order == Order.SET_IDENTIFIER:
            msg = "SET_IDENTIFIER"
        elif order == Order.GET_MIN_PWM:
            pwm = read_i16(f)
            msg = "GET_MIN_PWM {}".format(pwm)
        elif order == Order.SET_MIN_PWM:
            msg = "SET_MIN_PWM"
        elif order == Order.GET_MAX_PWM:
            pwm = read_i16(f)
            msg = "GET_MAX_PWM {}".format(pwm)
        elif order == Order.SET_MAX_PWM:
            msg = "SET_MAX_PWM"
        elif order == Order.GET_ZERO_RAW_POSITION:
            position = read_i8(f)
            msg = "GET_ZERO_RAW_POSITION {}".format(position)
        elif order == Order.SET_ZERO_RAW_POSITION:
            msg = "SET_ZERO_RAW_POSITION"
        elif order == Order.GET_GRAVITY_FEED_FORWARD:
            gravity_feedorward = read_i16(f)
            msg = "GET_GRAVITY_FEED_FORWARD {}".format(gravityFeedForward)
        elif order == Order.SET_GRAVITY_FEED_FORWARD:
            msg = "SET_GRAVITY_FEED_FORWARD"
        else:
            msg = ""
            print("Unknown Order", byte)

        if debug:
            print(msg)
    except Exception as e:
        print("Error decoding order {}: {}".format(byte, e))
        print('byte={0:08b}'.format(byte))
