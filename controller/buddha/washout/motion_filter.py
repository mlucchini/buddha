DELAY_MAX = 3

class MotionFilter:
    def __init__(self, sampling_interval, cutoff_frequency):
        """
        :param sampling_interval: in ms
        :param cutoff_frequency: in rad/s
        """
        self.sampling_interval = sampling_interval
        self.cutoff_frequency = cutoff_frequency
        self.input = [0.0] * DELAY_MAX
        self.output = [0.0] * DELAY_MAX
