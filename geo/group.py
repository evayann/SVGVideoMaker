
# region Imports
from geo.animation import AnimationType
from geo.quadrant import Quadrant
# endregion Imports

class Group:
    def __init__(self):
        self.group = []
        self.animations = self # Opaque structure to let user apply modification of animation on all a group.

    def add(self, *elements):
        for element in elements:
            self.group.append(element)

    def set_verbose(self, boolean):
        for element in self.group:
            element.animations.set_verbose(boolean)

    def init_animation(self):
        for element in self.group:
            element.animations.init_animation()

    def set_fps(self, fps):
        for element in self.group:
            element.animations.set_fps(fps)

    def add_animation_by_frame(self, frame, values, anim_type=AnimationType.TRANSLATION):
        if anim_type == AnimationType.MODIFICATION:
            raise Exception("Group can't have modification animation")

        for element in self.group:
            element.animations.add_animation_by_frame(frame, values, anim_type)

    def is_style(self):
        return False

    def get_end_time(self):
        end_time = -1
        for element in self.group:
            end_time = max(end_time, element.animations.end_time)
        return end_time

    def update(self):
        for element in self.group:
            element.animations.update()

    def display_animations(self):
        for element in self.group:
            element.animations.display_animations()

    def apply_translation(self, value):
        for element in self.group:
            element.animations.apply_translation(value)

    def apply_inflation(self, value):
        for element in self.group:
            element.animations.apply_inflation(value)

    def reset(self):
        for element in self.group:
            element.animations.reset()

    # region SVG
    def bounding_quadrant(self):
        """
        return min quadrant containing point.
        this method is defined on any displayable object.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for element in self.group:
            quadrant.update(element.bounding_quadrant())
        return quadrant

    def get_svg(self):
        """
        Return a string who describe the group
        :return: the string who describe group
        """
        return self.svg_content()

    def svg_content(self):
        """
        Return a string who describe the group
        :return: the string who describe group
        """
        string = "<g>"
        for el in self.group:
            string += el.svg_content()
        string += "</g>"
        return string
    # endregion SVG
