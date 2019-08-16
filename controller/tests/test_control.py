from __future__ import print_function, division, absolute_import
from unittest.mock import MagicMock

import pytest
import serial

from buddha.platform.vector import Vector
from buddha.serial.serial import Order
from buddha.control.control import Control
from buddha.platform.position import Position


def assert_eq(left, right):
    assert left == right, "{} != {}".format(left, right)


def mock_open_port_connected_identical_identifiers(serial_port, baudrate, timeout):
    mock = MagicMock(spec=serial.Serial)
    mock.read = MagicMock(side_effect=[[Order.CONNECTED.value], [Order.RECEIVED.value], [1], [Order.RECEIVED.value]])
    return mock


def mock_open_port_connected_with_identifiers(serial_port, baudrate, timeout):
    mock = MagicMock(spec=serial.Serial)
    mock.read = MagicMock(side_effect=[[Order.CONNECTED.value], [Order.RECEIVED.value], [int(serial_port[-1:])], [Order.RECEIVED.value], [Order.RECEIVED.value]])
    return mock


@pytest.mark.xfail(raises=RuntimeError)
def test_missing_serial_ports():
        Control(serial_ports=[])


@pytest.mark.xfail(raises=serial.serialutil.SerialException)
def test_incorrect_serial_ports():
        Control(serial_ports=["", "", "", "", "", ""])


@pytest.mark.xfail(raises=RuntimeError)
def test_connect_connected_order_received_identical_identifiers():
    control = Control(serial_ports=["cu.usbserial-0", "cu.usbserial-1", "cu.usbserial-2", "cu.usbserial-3", "cu.usbserial-4", "cu.usbserial-5"],
                      open_port=mock_open_port_connected_identical_identifiers)
    control.connect()


@pytest.mark.xfail(raises=RuntimeError)
def test_connect_connected_order_received_invalid_identifiers():
    control = Control(serial_ports=["cu.usbserial-9", "cu.usbserial-8", "cu.usbserial-7", "cu.usbserial-6", "cu.usbserial-5", "cu.usbserial-4"],
                      open_port=mock_open_port_connected_with_identifiers)
    control.connect()


def test_connect_connected_order_received_unique_valid_identifiers():
    control = Control(serial_ports=["cu.usbserial-2", "cu.usbserial-0", "cu.usbserial-1", "cu.usbserial-4", "cu.usbserial-3", "cu.usbserial-5"],
                      open_port=mock_open_port_connected_with_identifiers)
    control.connect()
    assert_eq(control.is_connected(), True)


def test_move():
    control = Control(serial_ports=["cu.usbserial-2", "cu.usbserial-0", "cu.usbserial-1", "cu.usbserial-4", "cu.usbserial-3", "cu.usbserial-5"],
                      open_port=mock_open_port_connected_with_identifiers)
    control.connect()
    control.move(Position(Vector(0.5, 0.5, 0.5), Vector(0.5, 0.5, 0.5)))
