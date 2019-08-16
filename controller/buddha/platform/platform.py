import math

import copy

from .vector import Vector

# Paper:
# https://web.archive.org/web/20130506134518/http://www.wokinghamu3a.org.uk/Maths%20of%20the%20Stewart%20Platform%20v5.pdf

# Notes:
# The position of servos zero to six increment clockwise
# The horizontal axis x "zero" is servo zero's arm ie. beta[0]
# The servo "0 degree reference" is servo arm pointing South, ie. at "home" it's either -90 or 90 degrees

# Both used to calculate b(i) in the paper
# The radius of the base ie. the distance between the base center and any shaft/arm intersection in plane x-y
# The angles between the horizontal axis x and shaft/arm intersections
DEFAULT_BASE_RADIUS = 275.0
DEFAULT_BASE_ANGLES = [63, 108, 183, 228, 303, 348]

# Both used to calculate p(i) in the paper
# The radius of the platform ie. the distance between the platform center and any universal joint in plane x-y
# The angles between the horizontal axis x and universal joints
DEFAULT_PLATFORM_RADIUS = 200.0
DEFAULT_PLATFORM_ANGLES = [80.5, 90.5, 200.5, 210.5, 320.5, 330.5]

DEFAULT_BETA = [0, 180, 120, 300, 240, 60]
DEFAULT_HORN_LENGTH = 100.0
DEFAULT_LEG_LENGTH = 330.0
DEFAULT_INITIAL_HEIGHT = 300.0

DEFAULT_MAX_TRANSLATION = 100.0
DEFAULT_MAX_ROTATION = math.pi / 4

VECTOR_SIZE_BOUND = 1.0


class Platform:
    def __init__(self, base_angles=DEFAULT_BASE_ANGLES, platform_angles=DEFAULT_PLATFORM_ANGLES,
                 beta=DEFAULT_BETA, initial_height=DEFAULT_INITIAL_HEIGHT, base_radius=DEFAULT_BASE_RADIUS,
                 platform_radius=DEFAULT_PLATFORM_RADIUS, horn_length=DEFAULT_HORN_LENGTH, leg_length=DEFAULT_LEG_LENGTH,
                 max_translation=DEFAULT_MAX_TRANSLATION, max_rotation=DEFAULT_MAX_ROTATION):
        # beta(i) in the paper
        # The angles between the horizontal axis x and each servo arm plane
        self.beta = list(map(math.radians, beta))

        # h(0) in the paper
        # Vector representing the height of the platform in the "home" position
        self.initial_height = Vector(0.0, 0.0, initial_height)

        # b(i) in the paper
        # The vectors between the base center and shaft/arm intersections
        self.base_joint = self.__compute_joint_vectors(base_radius, base_angles)

        # p(i) in the paper
        # The vectors between the platform center and universal joints
        self.platform_joint = self.__compute_joint_vectors(platform_radius, platform_angles)

        # a in the paper
        # The center-to-center distance between any shaft and its connected universal joint
        self.horn_length = horn_length

        # s in the paper
        # The center-to-center distance between the two universal joints of the rods
        self.leg_length = leg_length

        # Not in the paper
        # Too small and the platform will not translate much
        # Too large and the platform will not be able to satisfy the translational and angular displacements asked for
        self.max_translation = max_translation

        # Pi / 8 in the paper
        # Too small and the platform will not rotate much
        # Too large and the platform will not be able to satisfy the translational and angular displacements asked for
        self.max_rotation = max_rotation

        # alpha(i) in the paper
        # The angles between the horizontal axis x and each servo operating arm
        self.angles = [0.0] * 6

        # q(i) in the paper
        # The vectors between the base center and the anchor points P(i)
        self.q = [Vector() for _ in range(6)]

        # l(i) in the paper
        # The vectors between the anchor points B(i) and the anchor points P(i) ie. the legs
        self.l = [Vector() for _ in range(6)]

        self.translation = Vector()
        self.rotation = Vector()

    @staticmethod
    def __compute_joint_vectors(radius, angles):
        return [Vector(radius * math.cos(math.radians(angles[i])), radius * math.sin(math.radians(angles[i])), 0.0) for i in range(6)]

    def __compute_leg_lengths(self):
        for i in range(6):
            self.q[i].set(math.cos(self.rotation.z) * math.cos(self.rotation.y) * self.platform_joint[i].x + (-math.sin(self.rotation.z) * math.cos(self.rotation.x) + math.cos(self.rotation.z) * math.sin(self.rotation.y) * math.sin(self.rotation.x)) * self.platform_joint[i].y + (math.sin(self.rotation.z) * math.sin(self.rotation.x) + math.cos(self.rotation.z) * math.sin(self.rotation.y) * math.cos(self.rotation.x)) * self.platform_joint[i].z,
                          math.sin(self.rotation.z) * math.cos(self.rotation.y) * self.platform_joint[i].x + (math.cos(self.rotation.z) * math.cos(self.rotation.x) + math.sin(self.rotation.z) * math.sin(self.rotation.y) * math.sin(self.rotation.x)) * self.platform_joint[i].y + (-math.cos(self.rotation.z) * math.sin(self.rotation.x) + math.sin(self.rotation.z) * math.sin(self.rotation.y) * math.cos(self.rotation.x)) * self.platform_joint[i].z,
                          -math.sin(self.rotation.y) * self.platform_joint[i].x + math.cos(self.rotation.y) * math.sin(self.rotation.x) * self.platform_joint[i].y + math.cos(self.rotation.y) * math.cos(self.rotation.x) * self.platform_joint[i].z)

            self.q[i].add(self.translation).add(self.initial_height)
            self.l[i].set(self.q[i].x, self.q[i].y, self.q[i].z).sub(self.base_joint[i])

    def __compute_servo_angles(self):
        try:
            alphas = [0.0] * 6
            for i in range(6):
                l = self.l[i].mag_sq() - (self.leg_length * self.leg_length) + (self.horn_length * self.horn_length)
                m = 2 * self.horn_length * (self.q[i].z - self.base_joint[i].z)
                n = 2 * self.horn_length * (math.cos(self.beta[i]) * (self.q[i].x - self.base_joint[i].x) + math.sin(self.beta[i]) * (self.q[i].y - self.base_joint[i].y))
                alphas[i] = math.asin(l / math.sqrt(m * m + n * n)) - math.atan2(n, m)
        except ValueError:
            print("WARNING: this request will be ignored since angles cannot be computed for these values")
            return
        self.angles = [math.degrees(math.pi / 2 + alpha if i % 2 else -math.pi / 2 - alpha) for i, alpha in enumerate(alphas)]

    def update(self, position):
        position = copy.deepcopy(position)

        translation = position.translation
        rotation = position.rotation

        if not translation.bounded(VECTOR_SIZE_BOUND) or not rotation.bounded(VECTOR_SIZE_BOUND):
            print("WARNING: vector components provided are outside the allowed bounds (-1.0, 1.0)")
            return self.angles

        translation.multiply(self.max_translation)
        rotation.multiply(self.max_rotation)

        self.translation.set(translation.x, translation.y, translation.z)
        self.rotation.set(rotation.x, rotation.y, rotation.z)
        self.__compute_leg_lengths()
        self.__compute_servo_angles()

        return self.angles

    def get_angles(self):
        return self.angles

    def get_base_joints(self):
        return self.base_joint
