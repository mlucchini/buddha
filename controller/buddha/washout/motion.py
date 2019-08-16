class Motion:
    def __init__(self, translational_acceleration, rotational_velocity):
        """
        :param translational_acceleration: in m/s2
        :param rotational_velocity: in rad/s
        """
        self.translational_acceleration = translational_acceleration
        self.rotational_velocity = rotational_velocity

    def __str__(self):
        return "translational acceleration: [{}], rotational velocity: [{}]".format(self.translational_acceleration, self.rotational_velocity)
