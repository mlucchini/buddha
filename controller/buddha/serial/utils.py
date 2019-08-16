from __future__ import print_function, division, absolute_import

import sys
import glob

from buddha.serial.serial import read_order, Order, read_i8

try:
    import queue
except ImportError:
    import Queue as queue

import serial
import time


class CustomQueue(queue.Queue):
    def clear(self):
        with self.mutex:
            unfinished = self.unfinished_tasks - len(self.queue)
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.all_tasks_done.notify_all()
            self.unfinished_tasks = unfinished
            self.queue.clear()
            self.not_full.notify_all()


def get_serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/ttyUSB[0-9]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.wchusbserial*')
    else:
        raise EnvironmentError('Unsupported platform')

    results = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            results.append(port)
        except (OSError, serial.SerialException):
            pass
    return results


def open_serial_port(serial_port=None, baudrate=115200, timeout=0, write_timeout=0):
    if serial_port is None:
        serial_port = get_serial_ports()[0]

    # https://github.com/pyserial/pyserial/issues/59
    rts_cts = False if sys.platform.startswith('darwin') else True
    dsr_dtr = False if sys.platform.startswith('darwin') else True
    port = serial.Serial(port=serial_port, baudrate=baudrate, timeout=timeout, writeTimeout=write_timeout, rtscts=rts_cts, dsrdtr=dsr_dtr)

    # https://github.com/pyserial/pyserial/issues/329
    time.sleep(2)

    return port


def assert_order(serial_file, expected):
    error = ""
    actual = read_order(serial_file)
    if actual is Order.ERROR:
        error = read_i8(serial_file)
    assert actual == expected, "Orders do not match: {} != {} ({})".format(actual, expected, error)
