class Square:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.area = width * height

    def __repr__(self):
        return f"Width: {self.width}, Height: {self.height}"

    def is_equal(self, other):
        same = self.width == other.width and self.height == other.height
        same_flipped = self.width == other.height and self.height == other.width

        return same or same_flipped

class PlacedSquare(Square):
    def __init__(self, x_pos, y_pos, width, height):
        Square.__init__(self, width, height)

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.upper_left = x_pos, y_pos
        self.lower_right = x_pos + width, y_pos + height

    def __repr__(self):
        return f"{Square.__repr__(self)} at: {self.x_pos}, {self.y_pos}"

    def is_within(self, other_min, other_max):
        my_min = self.y_pos
        my_max = self.y_pos + self.height

        return max(my_min, other_min) < min(my_max, other_max)

    def check_overlap(self, other):
        a = min(self.lower_right[0], other.lower_right[0])
        b = max(self.upper_left[0], other.upper_left[0])
        c = max(0, a - b)
        d = min(self.lower_right[1], other.lower_right[1])
        e = max(self.upper_left[1], other.upper_left[1])
        f = max(0, d - e)

        return c * f