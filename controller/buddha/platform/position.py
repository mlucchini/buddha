class Position:
    def __init__(self, translation, rotation):
        self.translation = translation
        self.rotation = rotation

    def __str__(self):
        return "translation: [{}], rotation: [{}]".format(self.translation, self.rotation)

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.translation == other.translation and self.rotation == other.rotation
        return False

    def normalize_with(self, low, high):
        self.translation.normalize_with(low.translation, high.translation)
        self.rotation.normalize_with(low.rotation, high.rotation)
        return self
