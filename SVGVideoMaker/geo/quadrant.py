"""
Quadrants are rectangular boxes delimiting a set of items.
"""

class Quadrant:
    """
    enclosing rectangles.
    """
    def __init__(self, min_coordinates, max_coordinates):
        self.min_coordinates = list(min_coordinates)
        self.max_coordinates = list(max_coordinates)

    def copy(self):
        """
        return deepcopy of given quadrant.
        """
        return Quadrant(list(self.min_coordinates), list(self.max_coordinates))

    @classmethod
    def empty_quadrant(cls, dimension):
        """
        return an empty quadrant in space of given dimension
        """
        min_coordinates, max_coordinates = [], []
        for _ in range(dimension):
            min_coordinates.append(float('+inf'))
            max_coordinates.append(float('-inf'))
        return cls(min_coordinates, max_coordinates)

    def add_point(self, added_point):
        """
        register a point inside the quadrant.
        update limits if needed.
        """
        for i, added_coordinate in enumerate(added_point.coordinates):
            if added_coordinate < self.min_coordinates[i]:
                self.min_coordinates[i] = added_coordinate
            if added_coordinate > self.max_coordinates[i]:
                self.max_coordinates[i] = added_coordinate

    def update(self, other):
        """Expands self quadrant by taking constraints from other quadrant into account.
        The new one will have the minimal size needed to contain both initial ones.

        Args:
            other (Quadrant) : The other quadrant to update the self quadrant.
        """
        assert len(self.min_coordinates) == len(other.min_coordinates), \
            'merge in different spaces'
        for i, coordinate in enumerate(other.min_coordinates):
            if self.min_coordinates[i] > coordinate:
                self.min_coordinates[i] = coordinate
        for i, coordinate in enumerate(other.max_coordinates):
            if self.max_coordinates[i] < coordinate:
                self.max_coordinates[i] = coordinate

    def limits(self, index):
        """Returns tuple of limits for a given coordinate index.

        Args:
            index (int) : The index to get the limits.

        Returns:
            tuple : Returns tuple of limits for a given coordinate index.
        """
        return self.min_coordinates[index], self.max_coordinates[index]

    def intersect(self, other):
        """Get a boolean who indicate if the two quadrant have region in common.

        Args:
            other (Quadrant) : The other quadrant to check intersection.

        Returns:
            bool : True if intersect, otherwise False.
        """
        return all((mi1 < ma2 and ma1 > mi2) for mi1, mi2, ma1, ma2 in zip(self.min_coordinates, other.min_coordinates, self.max_coordinates, other.max_coordinates))

    def inflate(self, distance):
        """Get bigger quadrant containing original one + any point outside
        original at distance less than given.

        Args:
            distance (int) : The distance inflation to add at quadrant.
        """
        self.min_coordinates = [c - distance for c in self.min_coordinates]
        self.max_coordinates = [c + distance for c in self.max_coordinates]

    def inflate_factor(self, factor):
        """Get bigger quadrant by applying a multiplicative factor in each
        dimension, where 1 means "unchanged".

        Args:
            factor (int) : The factor of inflation to multiply at quadrant.
        """
        self.min_coordinates, self.max_coordinates = \
            zip(*[(cmin - (cmax - cmin) * (factor - 1) / 2,
                   cmax + (cmax - cmin) * (factor - 1) / 2)
                  for cmin, cmax in zip(self.min_coordinates, self.max_coordinates)])

    def devide(self):
        """Devide a quadrant in 4 equal subquadrant

        Returns:
            list : List of 4 subquadrant.
        """
        devided = []

        max_x, max_y = self.max_coordinates
        min_x, min_y = self.min_coordinates
        mid_x = (max_x - min_x) / 2 + min_x
        mid_y = (max_y - min_y) / 2 + min_y

        devided.append(Quadrant(self.min_coordinates, (mid_x, mid_y)))
        devided.append(Quadrant((min_x, mid_y), (mid_x, max_y)))
        devided.append(Quadrant((mid_x, min_y), (max_x, mid_y)))
        devided.append(Quadrant((mid_x, mid_y), self.max_coordinates))

        return devided

    def get_arrays(self):
        """Return tuple of min and max coordinate.

        Returns:
            tuple : Return tuple of min and max coordinate.
        """
        return self.min_coordinates, self.max_coordinates

    # region Override
    def __repr__(self):
        return f"{str(self)}\n"

    def __str__(self):
        return f"mi:x {round(self.min_coordinates[0],2)}, y {round(self.min_coordinates[1],2)} " \
               f"ma:x {round(self.max_coordinates[0],2)}, y {round(self.max_coordinates[1],2)}"
    # endregion Override
