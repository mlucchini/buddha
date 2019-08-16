import math

from buddha.platform.position import Position
from buddha.platform.vector import Vector

SECOND_IN_MS = 1000.0
GRAVITY_IN_MM = 9.80665 * 1000.0
DEFAULT_TRANSLATION_SCALE = 1.0
DEFAULT_ROTATION_SCALE = 1.0

# Papers:
# https://pdfs.semanticscholar.org/82d1/a36e9c6aca5bce4142856ed9ad97b79f291e.pdf
# https://www.researchgate.net/publication/261108151_Evaluation_of_motion_with_washout_algorithm_for_flight_simulator_using_tripod_parallel_mechanism
# https://duepublico2.uni-due.de/servlets/MCRFileNodeServlet/duepublico_derivate_00044467/Diss_Pham.pdf
# https://repository.tudelft.nl/view/aereports/uuid:45b071c0-0568-4e8f-948f-dfa52d350665


class WashoutFilter:
    def __init__(self, translation_high_pass_filters, translation_low_pass_filters, rotation_high_pass_filters, sampling_interval):
        """
        TODO: calibration
        TODO: limits
        :param sampling_interval: in ms
        """
        self.translation_high_pass_filters = translation_high_pass_filters
        self.translation_low_pass_filters = translation_low_pass_filters
        self.rotation_high_pass_filters = rotation_high_pass_filters
        self.sampling_interval = sampling_interval
        self.translation_scale = DEFAULT_TRANSLATION_SCALE
        self.rotation_scale = DEFAULT_ROTATION_SCALE
        self.translational_velocity = Vector()
        self.translation = Vector()
        self.rotation = Vector()
        self.rotation_no_tilt = Vector()
        self.tilt = Vector()
        self.platform_gravity = Vector()

    def __integrate(self, x, value):
        return x + (value * self.sampling_interval / SECOND_IN_MS)

    def __scale(self, motion):
        motion.translational_acceleration.multiply(self.translation_scale)
        motion.rotational_velocity.multiply(self.rotation_scale)

    def __translation(self, motion):
        translational_acceleration_with_gravity = motion.translational_acceleration + self.platform_gravity
        translational_acceleration_with_gravity.z -= GRAVITY_IN_MM

        translational_acceleration_high_pass = Vector(self.translation_high_pass_filters[0].apply(translational_acceleration_with_gravity.x),
                                                      self.translation_high_pass_filters[1].apply(translational_acceleration_with_gravity.y),
                                                      self.translation_high_pass_filters[2].apply(translational_acceleration_with_gravity.z))

        self.translational_velocity.set(self.__integrate(self.translational_velocity.x, translational_acceleration_high_pass.x),
                                        self.__integrate(self.translational_velocity.y, translational_acceleration_high_pass.y),
                                        self.__integrate(self.translational_velocity.z, translational_acceleration_high_pass.z))

        self.translation.set(self.__integrate(self.translation.x, self.translational_velocity.x),
                             self.__integrate(self.translation.y, self.translational_velocity.y),
                             self.__integrate(self.translation.z, self.translational_velocity.z))

    def __tilt_coordination(self, motion):
        translational_acceleration_low_pass = Vector(self.translation_low_pass_filters[0].apply(motion.translational_acceleration.x),
                                                     self.translation_low_pass_filters[1].apply(motion.translational_acceleration.y),
                                                     0.0)

        self.tilt.set(math.asin(translational_acceleration_low_pass.y / GRAVITY_IN_MM),
                      -math.asin(translational_acceleration_low_pass.x / GRAVITY_IN_MM),
                      0.0)

        if not -math.pi / 2 <= self.tilt.x <= math.pi / 2:
            self.tilt.x = math.pi / 2 if translational_acceleration_low_pass.y > 0 else -math.pi / 2

        if not -math.pi / 2 <= self.tilt.y <= math.pi / 2:
            self.tilt.y = math.pi / 2 if translational_acceleration_low_pass.x < 0 else -math.pi / 2

    def __rotation(self, motion):
        rotational_velocity_high_pass = Vector(self.rotation_high_pass_filters[0].apply(motion.rotational_velocity.x),
                                               self.rotation_high_pass_filters[1].apply(motion.rotational_velocity.y),
                                               self.rotation_high_pass_filters[2].apply(motion.rotational_velocity.z))

        self.rotation_no_tilt.x = self.__integrate(self.rotation_no_tilt.x, rotational_velocity_high_pass.x)
        self.rotation_no_tilt.y = self.__integrate(self.rotation_no_tilt.y, rotational_velocity_high_pass.y)
        self.rotation_no_tilt.z = self.__integrate(self.rotation_no_tilt.z, rotational_velocity_high_pass.z)

        self.rotation.reset().add(self.rotation_no_tilt).add(self.tilt)

    def __gravity(self):
        self.platform_gravity.set(-math.sin(self.rotation.y),
                                  math.sin(self.rotation.x) * math.cos(self.rotation.y),
                                  math.cos(self.rotation.x) * math.cos(self.rotation.y))
        self.platform_gravity.multiply(GRAVITY_IN_MM)

    def set_translation_scale(self, value):
        self.translation_scale = value

    def set_rotation_scale(self, value):
        self.rotation_scale = value

    def apply(self, motion):
        """
        :return: translation in meters and rotation in radians
        """
        self.__scale(motion)
        self.__translation(motion)
        self.__tilt_coordination(motion)
        self.__rotation(motion)
        self.__gravity()

        return Position(self.translation, self.rotation)
