from buddha.control.control import Control, Position
from flask import Flask, request
from objdict import ObjDict
from os import environ

from buddha.platform.vector import Vector

app = Flask(__name__)

control = Control()
control.connect()


@app.route("/configuration", methods=["POST"])
def configuration():
    # {"min_pwm": 30, "max_pwm": 255}
    content = request.json
    if 'min_pwm' in content:
        control.set_min_pwm(int(content['min_pwm']))
    if 'max_pwm' in content:
        control.set_max_pwm(int(content['max_pwm']))
    if 'gravity_feed_forward' in content:
        control.set_gravity_feed_forward(int(content['gravity_feed_forward']))
    return accepted()


@app.route("/reset", methods=["POST"])
def reset():
    control.reset()
    return accepted()


@app.route("/movement", methods=["POST"])
def movement():
    # {"translation": {"x": 0.5, "y": 0.5, "z": 0.5}, "rotation": {"x": 0.5, "y": 0.5, "z": 0.5}}
    position = to_position(request.json)
    control.move(position)
    return accepted()


@app.route("/animation", methods=["POST"])
def animation():
    #  {"keyframes": [{"position": {"translation": {"x": 0.5, "y": 0.5, "z": 0.5}, "rotation": {"x": 0.5, "y": 0.5, "z": 0.5}}, "delay": 2}]}
    content = request.json
    keyframes = [to_keyframe(keyframe) for keyframe in content['keyframes']]
    control.animation(keyframes)
    return accepted()


def to_keyframe(content):
    keyframe = ObjDict()
    keyframe.position = to_position(content['position'])
    keyframe.delay = content['delay']
    return keyframe


def to_position(content):
    translation = Vector(float(content['translation']['x']), float(content['translation']['y']), float(content['translation']['z']))
    rotation = Vector(float(content['rotation']['x']), float(content['rotation']['y']), float(content['rotation']['z']))
    return Position(translation, rotation)


def accepted():
    return '', 202


port = int(environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
