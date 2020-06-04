"""
Svg container for all svg element.
Useful to display and save all element.
"""
from itertools import cycle
from geo.quadrant import Quadrant


class SVG:
    """Container of all svg element.

     Args:
         elements (list) : List of svg element. Can be None.
         width    (int)  : Width in pixel of svg frame. Default 500.
         height   (int)  : Height in pixel of svg frame. Default 500.
     """
    svg_colors = 'red green blue purple orange saddlebrown mediumseagreen\
                       darkolivegreen lightskyblue dimgray mediumpurple midnightblue\
                       olive chartreuse darkorchid hotpink darkred peru\
                       goldenrod mediumslateblue orangered darkmagenta\
                       darkgoldenrod mediumslateblue firebrick palegreen\
                       royalblue tan tomato springgreen pink orchid\
                       saddlebrown moccasin mistyrose cornflowerblue\
                       darkgrey'.split()

    def __init__(self, elements=None, width=500, height=500):
        self.elements = []
        if elements:
            self.append(elements)
        self.svg_dimensions = (width, height)
        self.start_vb = None
        self.end_vb = None

    def init_animation(self):
        """
        Init all animations.
        """
        for element in self.elements:
            element.init_animation()

    def append(self, *elements):
        """Append all elements in svg.

        Args:
            *elements (list) : A list of all elements to add.
        """
        for element in elements:
            if isinstance(element, list):
                for el in element:
                    self.elements.append(el)
            else:
                self.elements.append(element)

    def save(self, path, name):
        """Save the svg frame.

        Args:
            path (str) : The path to save svg.
            name (str) : The name of svg.
        """
        f = open(f"{path}{name}.svg", "w")
        f.write(self.get_svg())
        f.close()

    def display_keys_animations(self):
        """
        Print all key animations of all svg element in svg.
        """
        for element in self.elements:
            print(element.display_animations())

    def update(self):
        """
        Update animation of all svg element in svg.
        """
        for element in self.elements:
            element.update()

    def reset(self):
        """
        Reset information about animation of all svg element in svg.
        """
        for element in self.elements:
            element.reset()

    def get_svg(self):
        """Compute svg to string.

        Returns:
            str: A string who describe the svg.
        """
        if self.start_vb and self.end_vb:
            vb = (self.start_vb.coordinates, self.end_vb.coordinates)
        else:
            quadrant = Quadrant.empty_quadrant(2)
            for element in self.elements:
                quadrant.update(element.bounding_quadrant())
            quadrant.inflate(1.1) # To see correctly border

            vb = quadrant.get_arrays()

        dimensions = [a - b for a, b in zip(vb[1], vb[0])]

        if any(d == 0.0 for d in dimensions):
            raise ValueError

        ratios = [a / b for a, b in zip(self.svg_dimensions, dimensions)]
        scale = min(ratios)
        if scale == 0.0:
            raise ValueError
        sk = 3 / scale
        return self.create_svg(view_box=vb, dimensions=dimensions, stroke_size=sk)

    def create_svg(self, view_box, dimensions, stroke_size):
        """Compute svg to string.

        Args:
            view_box    (tuple) : A tuple who describe the zone to display on svg. A simple view box.
            dimensions  (list)  : List of size (width and height).
            stroke_size (int)   : Size of stroke width of all element in svg.

        Returns:
            str: A string who describe the svg.
        """
        start = view_box[0]
        svg_file = '<svg width="{}" height="{}"'.format(*self.svg_dimensions)
        svg_file += ' viewBox="{} {}'.format(*start)
        svg_file += ' {} {}"'.format(*dimensions)
        svg_file += ' xmlns="http://www.w3.org/2000/svg">\n'
        svg_file += '<rect x="{}" y="{}"'.format(*start) # min size
        svg_file += ' width="{}" height="{}" fill="white"/>\n'.format(*dimensions)
        svg_file += '<g stroke-width="{}">\n'.format(stroke_size)
        svg_file += f"{self.compute_displays()}\n</g>\n </svg>\n"
        return svg_file

    def compute_displays(self):
        """
        Compute bounding quadrant and svg strings for all things to display.
        """
        strings = []
        for color, thing in zip(cycle(iter(SVG.svg_colors)), self.elements):
            if thing.is_style():
                strings.append('<g>\n')
            else:
                strings.append('<g fill="{}" stroke="{}">\n'.format(color, color))
            strings.append(thing.get_svg())
            strings.append('</g>\n')
        return " ".join(strings)

    # region Setters
    def set_verbose(self, boolean):
        for element in self.elements:
            element.set_verbose(boolean)

    def set_fps(self, fps):
        for element in self.elements:
            element.set_fps(fps)

    def set_size(self, width, height):
        self.svg_dimensions = (width, height)

    def set_view_box(self, start_point, end_point):
        self.start_vb = start_point
        self.end_vb = end_point
    # endregion Setters

    # region Getters
    def get_max_time(self):
        """Get the time of a movie.

        Returns:
            int : The time of last key frame.
        """
        max_time = 0
        for element in self.elements:
            max_time = max(element.get_end_time(), max_time)
        return max_time

    def get_nb_frames(self):
        """Get the number of frames.

        Returns:
            int : The id of last key frame.
        """
        nb_frame = 0
        for element in self.elements:
            nb_frame = max(element.get_nb_frames(), nb_frame)
        return nb_frame
    # endregion Getters

    # region Override
    def __str__(self):
        string = ""
        for element in self.elements:
            string += str(element)
        return string
    # endregion Override
