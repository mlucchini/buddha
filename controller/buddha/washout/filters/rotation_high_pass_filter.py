from buddha.washout.motion_filter import MotionFilter

SECOND_IN_MS = 1000.0

class RotationHighPassFilter(MotionFilter):
    def __init__(self, sampling_interval, cutoff_frequency):
        super().__init__(sampling_interval, cutoff_frequency)

    def __solve(self):
        tw = self.cutoff_frequency * self.sampling_interval / SECOND_IN_MS

        self.output[0] = 2.0 / (tw + 2) * (self.input[0] - self.input[1]) - (tw - 2) / (tw + 2) * self.output[1]

    def __delay(self):
        self.input[1] = self.input[0]
        self.output[1] = self.output[0]

    def apply(self, new_input):
        self.input[0] = new_input

        self.__solve()
        self.__delay()

        return self.output[0]
