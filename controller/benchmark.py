import random
import timeit

from buddha import Platform, Vector
from buddha.platform.position import Position


def make_and_transform_platform_randomly_n_times(n):
    platform = Platform()
    for i in range(n):
        position = Position(Vector(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)), Vector(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)))
        platform.update(position)


if __name__ == "__main__":
    """
    This script can be executed on a host computer (such as a Raspberry Pi) to benchmark its performance
    and make sure the host is fit for purpose.
    """
    print("Creating one platform and performing 1000 random updates")
    total = timeit.timeit("make_and_transform_platform_randomly_n_times(1000)", number=1, globals=globals())
    print("Total time: %f" % total)
    print("Time per update: %f" % (total / 1000))
