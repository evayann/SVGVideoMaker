
# region Imports
from geo.animation import AnimationType
from geo.quadrant import Quadrant
# endregion Imports

class Group:
    def __init__(self):
        self.group = []
        self.animations = self # Opaque structure to let user apply modification of animation on all a group.

    def append(self, *elements):
        """Append all elements in svg.

        Args:
            *elements (list) : A list of all elements to add.
        """
        for element in elements:
            if isinstance(element, list) or isinstance(element, tuple):
                for el in element:
                    self.group.append(el)
                    # self.animations.append(el.animations)
            else:
                self.group.append(element)
                # self.animations.append(element.animations)

    def init_animation(self):
        for el in self.group:
            if el.animations:
                el.animations.init_animation()

    def add_animation_by_frame(self, frame, values, anim_type=AnimationType.TRANSLATION):
        if anim_type == AnimationType.MODIFICATION:
            raise Exception("Group can't have modification animation")

        for el in self.group:
            if el.animations:
                el.animations.add_animation_by_frame(frame, values, anim_type)

    def is_style(self):
        return False

    def get_nb_frames(self):
        nb_frames = -1
        for el in self.group:
            nb_frames = max(nb_frames, el.animations.nb_frames)
        return nb_frames

    def get_keys_animations(self):
        """
        Get string of all key animations of all svg element in svg.
        """
        return "\n".join([el.animations.display_animations() for el in self.group if el.animations])

    def display_animations(self):
        """
        Get string of all key animations of all svg element in svg.
        """
        return "\n".join([el.animations.display_animations() for el in self.group if el.animations])

    def update(self):
        for el in self.group:
            if el.animations:
                el.animations.update()

    def apply_translation(self, value):
        for el in self.group:
            if el.animations:
                el.animations.apply_translation(value)

    def apply_inflation(self, value):
        for el in self.group:
            if el.animations:
                el.animations.apply_inflation(value)

    def reset(self):
        for el in self.group:
            if el.animations:
                el.animations.reset()

    # region SVG
    def bounding_quadrant(self):
        """Return a quadrant who contain the shape.

        Returns:
        	Quadrant: The quadrant who contain the shape.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for element in self.group:
            quadrant.update(element.bounding_quadrant())
        return quadrant

    def get_svg(self):
        """Return a string who describe shape only if it's visible.

        Returns:
            str: The string who describe the shape.
        """
        return self.svg_content()

    def svg_content(self):
        """Return a string who describe the shape.

        Returns:
            str: The string who describe the shape.
        """
        string = "<g>"
        for el in self.group:
            string += el.svg_content()
        string += "</g>"
        return string
    # endregion SVG

    # region Override
    def __str__(self):
        string = ""
        for element in self.group:
            string += f">{repr(element)}\n"
        return string

    def __repr__(self):
        return self.__class__.__name__
    # endregion Override
