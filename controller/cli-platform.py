from buddha.control.control import Control
from buddha.platform.platform import Vector
from buddha.platform.position import Position
from objdict import ObjDict

USAGE = "Available commands:\n" \
        "   move <translation: -1...1 -1...1 -1...1> <rotation: -1...1 -1...1 -1...1>\n" \
        "   angle <-180...180>\n" \
        "   set_min_pwm <0...255>\n" \
        "   set_max_pwm <0...255>\n" \
        "   set_gravity_feed_forward <0...255>\n" \
        "   calibrate\n" \
        "   stream\n" \
        "   animation <translation: -1...1 -1...1 -1...1> <rotation: -1...1 -1...1 -1...1> delay ...\n" \
        "   reset\n"

if __name__ == "__main__":
    """
    This tool is used to communicate with the whole platform, ie. all servos together.
    """

    print(USAGE)

    control = Control()
    control.connect()

    while True:
        try:
            instruction = input("Enter a command: ").strip()
            command, *arguments = instruction.split(" ")
            if command == "move" or command == "m":
                #  Lying down: move 0 0 0 0 0.2 0
                #  Sitting down: move 0 0 0 0.2 0.4 0
                translation = Vector(float(arguments[0]), float(arguments[1]), float(arguments[2]))
                rotation = Vector(float(arguments[3]), float(arguments[4]), float(arguments[5]))
                position = Position(translation, rotation)
                control.move(position)
            elif command == "angle" or command == "a":
                angle = int(arguments[0])
                control.move_motors_to_angle(angle)
            elif command == "set_min_pwm" or command == "smip":
                pwm = int(arguments[0])
                control.set_min_pwm(pwm)
            elif command == "set_max_pwm" or command == "smap":
                pwm = int(arguments[0])
                control.set_max_pwm(pwm)
            elif command == "set_gravity_feed_forward" or command == "sgff":
                feed_forward = int(arguments[0])
                control.set_gravity_feed_forward(feed_forward)
            elif command == "calibrate" or command == "c":
                Control.calibrate()
            elif command == "stream" or command == "s":
                control.sensor_stream()
            elif command == "animation" or command == "a":
                #  Roll: animation 0 0 0 0.2 0 0 0.5 0 0 0 -0.2 0 0 0.5
                #  Sway: animation 0.5 0 0 0 0 0 0.6 -0.5 0 0 0 0 0 0.6
                #  Heave: animation 0 0 0.3 0 0 0 0.7 0 0 -0.3 0 0 0 0.7
                keyframes = []
                for i in range(0, len(arguments), 7):
                    keyframe = ObjDict()
                    translation = Vector(float(arguments[i]), float(arguments[i + 1]), float(arguments[i + 2]))
                    rotation = Vector(float(arguments[i + 3]), float(arguments[i + 4]), float(arguments[i + 5]))
                    keyframe.position = Position(translation, rotation)
                    keyframe.delay = float(arguments[i + 6])
                    keyframes.append(keyframe)
                print(keyframes)
                control.animation(keyframes)
            elif command == "reset" or command == "r":
                control.reset()
            else:
                print("Unrecognized command")
                print(USAGE)
        except (IndexError, ValueError) as e:
            print("Error: %s" % e)
            print(USAGE)
            continue
