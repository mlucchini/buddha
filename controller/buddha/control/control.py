import json
import socket

import time

from buddha.platform.platform import Platform
from buddha.platform.position import Position
from buddha.platform.vector import Vector
from buddha.serial.serial import Order, write_order, read_i8, write_i16
from buddha.serial.utils import open_serial_port, get_serial_ports, assert_order

SERIAL_PORT_PREFIXES = ("/dev/tty.wchusbserial", "/dev/ttyUSB")
DEFAULT_BAUD_RATE = 115200
NB_SERVOS = 6

LOWER_BOUNDS = Position(Vector(-4.16, -4.24, -8.19), Vector(-0.26, -0.30, -0.998))
HIGHER_BOUNDS = Position(Vector(5.94, 3.92, 7.08), Vector(0.38, 0.59, 0.999))

SENSOR_INPUT_TCP_IP = '0.0.0.0'
SENSOR_INPUT_TCP_PORT = 8888


class Control:
    def __init__(self, open_port=open_serial_port, serial_ports=None, baud_rate=DEFAULT_BAUD_RATE, platform=Platform()):
        self.serial_ports = serial_ports if serial_ports is not None else list(filter(lambda p: p.startswith(SERIAL_PORT_PREFIXES), get_serial_ports()))
        if len(self.serial_ports) != NB_SERVOS:
            raise RuntimeError("Expected %d servos; found %d serial ports" % (NB_SERVOS, len(self.serial_ports)))
        print("Opening ports...")
        self.serial_files = [open_port(serial_port=serial_port, baudrate=baud_rate, timeout=None) for serial_port in self.serial_ports]
        self.baud_rate = baud_rate
        self.platform = platform
        self.connected = [False] * NB_SERVOS
        self.identifiers = [-1] * NB_SERVOS

    def __connect_one(self, index):
        print("Sending 'hello' to servo %s..." % index)
        serial_file = self.serial_files[index]
        serial_file.reset_input_buffer()
        serial_file.reset_output_buffer()

        write_order(serial_file, Order.HELLO)

        print("Waiting for 'connected' from servo %s..." % index)
        assert_order(serial_file, Order.CONNECTED)
        assert_order(serial_file, Order.RECEIVED)

        write_order(serial_file, Order.GET_IDENTIFIER)
        identifier = read_i8(serial_file)
        assert_order(serial_file, Order.RECEIVED)

        if identifier < 0 or identifier > NB_SERVOS - 1 or identifier in self.identifiers:
            raise RuntimeError("Servo with serial port '%s' has the invalid or duplicate identifier '%s'. Please set it correctly using the SET_IDENTIFIER order" % (self.serial_ports[index], identifier))
        self.identifiers[index] = identifier
        self.connected[index] = True

    def __move_one(self, index, identifier, angle):
        i16_angle = int(angle)

        print("Servo %d will be moved to %d" % (identifier, i16_angle))

        serial_file = self.serial_files[index]
        write_order(serial_file, Order.SET_SERVO_ANGLE)
        write_i16(serial_file, i16_angle)
        assert_order(serial_file, Order.RECEIVED)

    def connect(self):
        for index in range(NB_SERVOS):
            if not self.connected[index]:
                self.__connect_one(index)

        if self.is_connected:
            print("Ready and connected to all the servos")
        else:
            raise RuntimeError("Could not connect to all servos")

    def is_connected(self):
        return all(self.connected)

    def move(self, position):
        print("Move platform to position %s requested" % position)

        angles = self.platform.update(position)

        for index in range(NB_SERVOS):
            identifier = self.identifiers[index]
            angle = angles[identifier]
            self.__move_one(index, identifier, angle)

    def move_motors_to_angle(self, angle):
        print("Move motors to angle %s requested" % angle)

        for index in range(NB_SERVOS):
            self.__move_one(index, index, angle)

    @staticmethod
    def calibrate():
        print("Move the input device in a realistic fashion in order to allow the calculation of pertinent limits for"
              "both rotation and translation. Limits will then be printed. Hit Ctrl-C to end the calibration.\n")
        print("Waiting for a sensor stream on %s:%s..." % (SENSOR_INPUT_TCP_IP, SENSOR_INPUT_TCP_PORT))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SENSOR_INPUT_TCP_IP, SENSOR_INPUT_TCP_PORT))
        s.listen(1)
        connection, address = s.accept()
        low = Position(Vector(), Vector())
        high = Position(Vector(), Vector())
        try:
            while True:
                data = connection.recv(256)
                if not data: break
                json_data = json.loads(data)
                linear_acceleration = json_data["linearAcceleration"]["value"]
                rotation_vector = json_data["rotationVector"]["value"]
                low.translation.set(min(low.translation.x, linear_acceleration[0]),
                                    min(low.translation.y, linear_acceleration[1]),
                                    min(low.translation.z, linear_acceleration[2]))
                low.rotation.set(min(low.rotation.x, rotation_vector[0]),
                                 min(low.rotation.y, rotation_vector[1]),
                                 min(low.rotation.z, rotation_vector[2]))
                high.translation.set(max(high.translation.x, linear_acceleration[0]),
                                     max(high.translation.y, linear_acceleration[1]),
                                     max(high.translation.z, linear_acceleration[2]))
                high.rotation.set(max(high.rotation.x, rotation_vector[0]),
                                  max(high.rotation.y, rotation_vector[1]),
                                  max(high.rotation.z, rotation_vector[2]))
                print("Lower bounds: %s" % low)
                print("Higher bounds: %s" % high)
        except KeyboardInterrupt:
            pass
        finally:
            connection.close()

    def sensor_stream(self):
        # TODO: Consume on a different thread to make sure we don't build a backlog?
        print("Wait for a sensor stream on %s:%s..." % (SENSOR_INPUT_TCP_IP, SENSOR_INPUT_TCP_PORT))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SENSOR_INPUT_TCP_IP, SENSOR_INPUT_TCP_PORT))
        s.listen(1)
        connection, address = s.accept()
        while True:
            data = connection.recv(256)
            if not data: break
            json_data = json.loads(data)
            linear_acceleration = json_data["linearAcceleration"]["value"]
            rotation_vector = json_data["rotationVector"]["value"]
            translation = Vector(linear_acceleration[0], linear_acceleration[1], linear_acceleration[2])
            rotation = Vector(rotation_vector[0], rotation_vector[1], rotation_vector[2])
            position = Position(translation, rotation)
            position.normalize_with(LOWER_BOUNDS, HIGHER_BOUNDS)
            self.move(position)
        connection.close()

    def animation(self, keyframes):
        print("Hit Ctrl-C to end the animation.\n")
        try:
            keyframe_index = 0
            while True:
                keyframe = keyframes[keyframe_index]
                self.move(keyframe.position)
                time.sleep(keyframe.delay)
                keyframe_index = (keyframe_index + 1) % len(keyframes)
        except KeyboardInterrupt:
            pass

    def reset(self):
        self.move(Position(Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0)))

    def set_min_pwm(self, pwm):
        print("The servos min PWM will be set to %d temporarily" % pwm)
        for index in range(NB_SERVOS):
            serial_file = self.serial_files[index]
            write_order(serial_file, Order.SET_MIN_PWM)
            write_i16(serial_file, pwm)
            assert_order(serial_file, Order.RECEIVED)

    def set_max_pwm(self, pwm):
        print("The servos max PWM will be set to %d temporarily" % pwm)
        for index in range(NB_SERVOS):
            serial_file = self.serial_files[index]
            write_order(serial_file, Order.SET_MAX_PWM)
            write_i16(serial_file, pwm)
            assert_order(serial_file, Order.RECEIVED)

    def set_gravity_feed_forward(self, feed_forward):
        print("The servos gravity feed forward will be set to %d temporarily" % feed_forward)
        for index in range(NB_SERVOS):
            serial_file = self.serial_files[index]
            write_order(serial_file, Order.SET_GRAVITY_FEED_FORWARD)
            write_i16(serial_file, feed_forward)
            assert_order(serial_file, Order.RECEIVED)
