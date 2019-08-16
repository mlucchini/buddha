from buddha.serial.serial import read_i8, write_i16, write_i8, read_i16
from buddha.control.control import open_serial_port, Order, write_order, assert_order
from buddha.serial.utils import get_serial_ports

SERIAL_PORT_PREFIX = "/dev/tty.wchusbserial"
USAGE = "Available commands:\n" \
        "   get_identifier\n" \
        "   set_identifier <0...5> (stored in EEPROM)\n" \
        "   get_zero_raw_position\n" \
        "   set_zero_raw_position (stored in EEPROM)\n" \
        "   get_servo_angle\n" \
        "   set_servo_angle <-180...180> (volatile)\n" \
        "   get_min_pwm\n" \
        "   set_min_pwm <0...255> (volatile)\n" \
        "   get_max_pwm\n" \
        "   set_max_pwm <0...255> (volatile)\n" \
        "   get_gravity_feed_forward\n" \
        "   set_gravity_feed_forward (volatile)\n"


if __name__ == "__main__":
    """
    This tool is used to communicate with a single servo.
    Used for configuration and troubleshooting purposes.
    """

    serial_ports = list(filter(lambda p: p.startswith(SERIAL_PORT_PREFIX), get_serial_ports()))
    if len(serial_ports) != 1:
        raise RuntimeError("Found %d ports matching prefix %s" % (len(serial_ports), SERIAL_PORT_PREFIX))

    serial_port = serial_ports[0]
    serial_file = open_serial_port(serial_port=serial_port, baudrate=115200, timeout=None)

    print("Connection to the servo...")
    write_order(serial_file, Order.HELLO)
    assert_order(serial_file, Order.CONNECTED)
    assert_order(serial_file, Order.RECEIVED)
    print("Connected to the servo")

    print(USAGE)

    while True:
        instruction = input("Enter a command: ").strip()
        command, *arguments = instruction.split(" ")
        if command == "get_identifier" or command == "gi":
            write_order(serial_file, Order.GET_IDENTIFIER)
            print(read_i8(serial_file))
            assert_order(serial_file, Order.RECEIVED)
            print("Success")
        elif command == "set_identifier" or command == "si":
            write_order(serial_file, Order.SET_IDENTIFIER)
            write_i8(serial_file, int(arguments[0]))
            assert_order(serial_file, Order.RECEIVED)
            print("Success")
        elif command == "get_servo_angle" or command == "gsa":
            write_order(serial_file, Order.GET_SERVO_ANGLE)
            print(read_i16(serial_file))
            assert_order(serial_file, Order.RECEIVED)
            print("Success")
        elif command == "set_servo_angle" or command == "ssa":
            write_order(serial_file, Order.SET_SERVO_ANGLE)
            write_i16(serial_file, int(arguments[0]))
            assert_order(serial_file, Order.RECEIVED)
            print("Success")
        elif command == "get_min_pwm" or command == "gmip":
            write_order(serial_file, Order.GET_MIN_PWM)
            print(read_i16(serial_file))
            assert_order(serial_file, Order.RECEIVED)
            print("Success")
        elif command == "set_min_pwm" or command == "smip":
            write_order(serial_file, Order.SET_MIN_PWM)
            write_i16(serial_file, int(arguments[0]))
            assert_order(serial_file, Order.RECEIVED)
            print("Success")
        elif command == "get_max_pwm" or command == "gmap":
            write_order(serial_file, Order.GET_MAX_PWM)
            print(read_i16(serial_file))
            assert_order(serial_file, Order.RECEIVED)
            print("Success")
        elif command == "set_max_pwm" or command == "smap":
            write_order(serial_file, Order.SET_MAX_PWM)
            write_i16(serial_file, int(arguments[0]))
            assert_order(serial_file, Order.RECEIVED)
            print("Success")
        elif command == "get_zero_raw_position" or command == "gzrp":
            write_order(serial_file, Order.GET_ZERO_RAW_POSITION)
            print(read_i8(serial_file))
            assert_order(serial_file, Order.RECEIVED)
            print("Success")
        elif command == "set_zero_raw_position" or command == "szrp":
            write_order(serial_file, Order.SET_ZERO_RAW_POSITION)
            assert_order(serial_file, Order.RECEIVED)
            print("Success")
        elif command == "get_gravity_feed_forward" or command == "ggff":
            write_order(serial_file, Order.GET_GRAVITY_FEED_FORWARD)
            print(read_i16(serial_file))
            assert_order(serial_file, Order.RECEIVED)
            print("Success")
        elif command == "set_gravity_feed_forward" or command == "sgff":
            write_order(serial_file, Order.SET_GRAVITY_FEED_FORWARD)
            write_i16(serial_file, int(arguments[0]))
            assert_order(serial_file, Order.RECEIVED)
            print("Success")
        else:
            print("Unrecognized command")
            print(USAGE)
