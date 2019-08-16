def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def constrain(x, low, high):
    return low if x < low else high if x > high else x
