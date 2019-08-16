import math

from buddha.washout.motion_filter import MotionFilter

SECOND_IN_MS = 1000.0

class TranslationLowPassFilter(MotionFilter):
    def __init__(self, sampling_interval, cutoff_frequency, damping_ratio):
        super().__init__(sampling_interval, cutoff_frequency)
        self.damping_ratio = damping_ratio

    def __solve(self):
        t2w2 = math.pow(self.cutoff_frequency * self.sampling_interval / SECOND_IN_MS, 2)
        dw4t = 4.0 * self.damping_ratio * self.cutoff_frequency * self.sampling_interval / SECOND_IN_MS

        self.output[0] = t2w2 / (t2w2 + dw4t + 4) * (self.input[0] + 2 * self.input[1] + self.input[2]) - (1.0 / (t2w2 + dw4t + 4)) * (2.0 * (t2w2 - 4) * self.output[1] + (t2w2 - dw4t + 4) * self.output[2])

    def __delay(self):
        self.input[2] = self.input[1]
        self.input[1] = self.input[0]

        self.output[2] = self.output[1]
        self.output[1] = self.output[0]

    def apply(self, new_input):
        self.input[0] = new_input

        self.__solve()
        self.__delay()

        return self.output[0]
