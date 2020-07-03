
# region Imports
from SVGVideoMaker.geo.animation import AnimationType
from SVGVideoMaker.geo.quadrant import Quadrant
from SVGVideoMaker.geo.style import Style
# endregion Imports

class Group:
    """
    Initialize Group
    """
    def __init__(self):
        self.group = []
        self.animations = self # Opaque structure to let user apply modification of animation on all a group.
        self.translation = [0, 0]
        self.rotation = 0
        self.style = Style(opacity=1)

    def append(self, *elements):
        """Append all elements in svg.

        Args:
            *elements (list) : A list of all elements to add.
        """
        for element in elements:
            if isinstance(element, list) or isinstance(element, tuple):
                for el in element:
                    self.group.append(el)
            else:
                self.group.append(element)

    def init_animation(self):
        for el in self.group:
            if el.animations:
                el.animations.init_animation()

    def add_animation(self, frame, anim_type=AnimationType.TRANSLATION, x=None, y=None, value=None):
        if anim_type == AnimationType.MODIFICATION:
            raise Exception("Group can't have modification animation")

        for el in self.group:
            if el.animations:
                if value:
                    el.animations.add_animation(frame, anim_type, value=value)
                elif x and y:
                    el.animations.add_animation(frame, anim_type, x=x, y=y)

    def set_style(self, fill_color=None, stroke_color=None, stroke_width=None, stroke_linecaps=None,
                  stroke_dasharray=None, opacity=None, others_rules=None, custom=True):
        """Set the style of a svg element.

		Args:
			fill_color       (str)    : The color to fill shape.
			stroke_color     (str)    : The color of stroke of the shape.
			stroke_width     (float)  : The size of stroke of the shape.
			stroke_dasharray (str)    : The string who describe the dasharray of the shape.
			opacity          (float)  : The opacity of shape.
			custom           (bool)   : A bool who indicate if we set a default style or if it's custom.
		"""
        if self.style is None:
            self.style = Style()
        self.style.set(fill_color, stroke_color, stroke_width, stroke_linecaps, stroke_dasharray, opacity, custom)
        if others_rules:
            self.style.add_other_rules(others_rules)

    def add_other_rule(self, rules):
        """Add new rules at previous others rules.
		Can be str or list

		Args:
			rules (str or list) : The rules to add.
		"""
        if self.style:
            self.style.add_other_rules(rules)

    def is_style(self):
        return self.style.custom if self.style else False

    def get_transform(self):
        """Get a string who describe all transform.

		Returns:
			str: The string who describe transform of this shape.
		"""
        translation = " ".join([str(el) for el in self.translation])
        string = f'transform="translate({translation})'
        # TODO Not supported yet need to have center rotation
        # if self.rotation != 0:
        #     center_pt = "{} {}".format(*self.get_center())
        #     string += f" rotate({self.rotation} {center_pt})"

        return string + '"'

    def get_nb_frames(self):
        nb_frames = -1
        for el in self.group:
            nb_frames = max(nb_frames, el.animations.get_nb_frames())
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

    def add_translation(self, frame, x, y=None):
        """Add translation animation on shape at frame.

		Args:
			frame (int): The frame.
			x     (int): The translation on X axis.
			y     (int): The translation on Y axis.
		"""
        for el in self.group:
            if el.animations:
                el.add_rotate(frame, x=x, y=y)

    def add_rotate(self, frame, value):
        """Add rotation animation on shape at frame.

		Args:
			frame (int): The frame.
			value (float): The rotation in degrees.
		"""
        for el in self.group:
            if el.animations:
                el.add_rotate(frame, value=value)

    def add_opacity(self, frame, value):
        """Add opacity animation on shape at frame.

		Args:
			frame (int): The frame.
			value (float): The percent of opacity. Between 0 and 1.
		"""
        for el in self.group:
            if el.animations:
                el.add_opacity(frame, value)

    def add_inflation(self, frame, x, y=None):
        """Add translation animation on shape at frame.

		Args:
			frame (int): The frame.
			x     (int): The inflation on X axis.
			y     (int): The inflation on Y axis.
		"""
        for el in self.group:
            if el.animations:
                el.add_inflation(frame, x, y)

    def apply_translation(self, value):
        for el in self.group:
            if el.animations:
                el.animations.apply_translation(value)

    def apply_inflation(self, value):
        for el in self.group:
            if el.animations:
                el.animations.apply_inflation(value)

    def apply_opacity(self, value):
        for el in self.group:
            if el.animations:
                el.animations.apply_opacity(value)

    def apply_rotate(self, value):
        # TODO Change center
        for el in self.group:
            if el.animations:
                el.animations.apply_rotate(value)

    def reset(self):
        for el in self.group:
            if el.animations:
                el.reset()

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
        string = f"<g {self.get_transform()} {self.style.get_styles()}>"
        for el in self.group:
            string += el.svg_content() + "\n"
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

    def __iter__(self):
        yield from self.get_child(self.group)

    def get_child(self, group):
        for child in group:
            yield child
            if isinstance(child, Group):
                yield from self.get_child(child)
    # endregion Override
