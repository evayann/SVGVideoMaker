
# region Imports
from enum import Enum
from copy import deepcopy
from SVGVideoMaker.geo.debug import msg, DebugLevel
# endregion Imports


class AnimationType(Enum):
    """
    Enumeration of different type of animation.
    """
    TRANSLATION = 1
    MODIFICATION = 2
    INFLATION = 3
    ROTATION = 4
    OPACITY = 5
    ANGLE_TRANSLATION = 6

class AnimationState(Enum):
    """
    Enumeration of different state of animation.
    """
    NEW = 0
    CURRENT = 1
    END = 2

class Animation:
    """
    Animation
    """

    # Define value for save/get current values of all types
    KEY, VALUES = 0, 1

    def __init__(self, svg_element, id=None):
        """Animation for all types (Translation, Inflation, Reshape, Opacity)

        Args:
            svg_element (Shape) : The element to animate.
            id          (str)   : An identifier of animation.
        """
        self.svg_el = svg_element
        self.id = id if id else None
        self.current_frame = 0

        self.anims = dict()
        for anim_type in AnimationType:
            self.anims[anim_type] = dict() # Position of element with second in key

        self.anim_computed = None

        self.current_values = dict()
        for anim_type in AnimationType:
            self.current_values[anim_type] = (-1, None) # Initialization

        self.nb_frames = 0

    def set_start(self, opacity):
        self.anims[AnimationType.OPACITY][0] = opacity # Add the init display for DISPLAY

    def init_animation(self):
        self.anim_computed = deepcopy(self.anims)

    def finish_animation(self):
        self.anim_computed = None # Clear element computed

    def add_animation(self, frame, anim_type=AnimationType.TRANSLATION, **kwargs):
        """Add animation pn the good type and check if data is ok

        Args:
            frame     (int)          : The frame number.
            anim_type (AnimationType): The type of animation to add.
            **kwargs                 : The data to add. Attribute can be x, y or value.
        """
        # Check the data type and do some checking operation before
        if len(kwargs) == 2:
            from SVGVideoMaker.geo.point import Point2D
            values = Point2D(kwargs["x"], kwargs["y"])
        else:
            values = kwargs["value"]

        # Add data if is good
        self.anims[anim_type][frame] = deepcopy(values) # To don't be affect about possible modification
        self.nb_frames = max(frame, self.nb_frames)

    def update(self):
        """
        Update all animation, modification need to be in first.
        """
        self.update_translation()
        self.update_inflation()
        self.update_rotation()
        self.update_opacity()
        # Increment frame counter
        self.current_frame += 1

    def read_animation(self, anim_type, force=False):
        """Read the animation to compute and return the previous animation values with his key frame.

        Args:
            anim_type (AnimationType) : The type of animation to read (in AnimationType).
            force     (bool)          : Oblige to search animation, if false can use element in save memory.

        Returns:
            AnimationState, (AnimationData, int), (AnimationData, int) :
                The previous animation values with his key time and also the next animations values and his key time.
        """
        if self.current_frame == 0:
            return AnimationState.END, (None, 0), (None, 0)  # Nothings at begin, it like if animation is finish

        if self.current_frame > self.current_values[anim_type][Animation.KEY] or force:
            # Search next animation data
            previous_anim, previous_frame = None, 0
            try:
                for key_frame, animation in self.anim_computed[anim_type].items():
                    # We pass the value
                    if self.current_frame <= key_frame:
                        return AnimationState.NEW, (previous_anim, previous_frame), (animation, key_frame)
                    # Set previous element
                    previous_anim = animation
                    previous_frame = key_frame
                else:
                    # End of animation
                    return AnimationState.END, (None, 0), (None, 0)
            except StopIteration:
                # No animation for this element
                return AnimationState.END, (None, 0), (None, 0)
        else:  # We have already the next animation data
            return AnimationState.CURRENT, (None, None), (None, None)

    def update_generic(self, anim_type, apply, sub=False):
        # Read values of Animation type
        state, (start_val, start_frame), (end_val, end_frame) = self.read_animation(anim_type)
        if state is AnimationState.NEW:
            # Compute addition and memoize for optimization
            value = end_val - start_val if sub else end_val
            self.current_values[anim_type] = (end_frame, value / (end_frame - start_frame))
        if state is not AnimationState.END:
            apply(self.current_values[anim_type][Animation.VALUES])

    def update_translation(self):
        self.update_generic(AnimationType.TRANSLATION, self.svg_el.apply_translation)

    def update_inflation(self):
        self.update_generic(AnimationType.INFLATION, self.svg_el.apply_inflation)

    def update_rotation(self):
        self.update_generic(AnimationType.ROTATION, self.svg_el.apply_rotation)

    def update_opacity(self):
        self.update_generic(AnimationType.OPACITY, self.svg_el.apply_opacity, sub=True)

    def reset(self):
        """
        Reset all animations.
        """
        # Reset frame counter
        self.current_frame = 0

    # region Getters
    def get_nb_frames(self):
        """Get the number of frames.

        Returns:
            int : The number of frames.
        """
        return self.nb_frames
    # endregion Getters

    def display_animations(self):
        """Compute information about the animation (key frame and values).

        Returns:
            str : String who describe all animations types.
        """
        string = f"ID : {self.id}, Nb frames:{self.nb_frames}\n"
        for anim_type in AnimationType:
            string += f"\t{anim_type} : \n"

            # Get the number of digit for a nice format
            nb_key = len(str(self.nb_frames))
            nb_values = len(str(len(self.anims[anim_type].values())))
            have_element = False

            for key, values in self.anims[anim_type].items():
                string += f"\t\t>Frame: {key:{nb_key}},"
                if anim_type is AnimationType.MODIFICATION and isinstance(values, list):
                    string += f"Size:{len(values):{nb_values}}, {str(values)}\n"
                else:
                    string += f"{values}\n"
                have_element = True

            if not have_element:
                string += "\t\t>Empty\n"

        return string

    # region Override
    def __str__(self):
        self.display_animations()
    # endregion Override

class ModificationAnimation(Animation):
    def __init__(self, svg_element, id=None):
        """Animation for all types (Translation, Inflation, Reshape, Opacity)

        Args:
            svg_element (Shape) : The element to animate.
            id          (str)   : An identifier of animation.
        """
        super().__init__(svg_element, id=id)

    def set_start(self, opacity, modifications_points):
        super().set_start(opacity)
        self.anims[AnimationType.MODIFICATION][0] = modifications_points  # Add the init_point for MODIFICATION

    def update_modification(self):
        state, (previous_val, start_frame), (next_val, end_frame) = self.read_animation(AnimationType.MODIFICATION)
        if state is AnimationState.NEW:
            if len(previous_val) != len(next_val):
                msg(f"Not same size between key: {start_frame} and key: {end_frame} !", DebugLevel.VERBOSE)

                # Simplify writing
                anims = self.anim_computed[AnimationType.MODIFICATION]

                # Not same number of point, need to reshape element before add element
                if len(previous_val) > len(next_val):
                    # Don't need to apply reshape because we have more points than necessary
                    anims[end_frame] = self.svg_el.reshape(next_val, previous_val)
                else:
                    # Need to apply the reshape because we need more points to match with next values
                    anims[start_frame] = self.svg_el.reshape(previous_val, next_val, apply=True)

                # Get new values who are reshape
                _, (previous_val, start_frame), (next_val, end_frame) = \
                    self.read_animation(AnimationType.MODIFICATION, force=True)

            # Compute the difference between previous and next position
            nb_frame_to_move = end_frame - start_frame
            computed = [((n - p) / nb_frame_to_move) for n, p in zip(next_val, previous_val)]
            # Save incrementation to add from start to end frame
            self.current_values[AnimationType.MODIFICATION] = end_frame, computed
            # Send the modification to add
            self.svg_el.apply_modification(computed)
        elif state is AnimationState.CURRENT:
            # Send modification
            self.svg_el.apply_modification(self.current_values[AnimationType.MODIFICATION][Animation.VALUES])

    def update(self):
        """
        Override update of Animation
        """
        # Proceeded
        self.update_modification()
        super().update()

class EllispePartAnimation(Animation):
    def __init__(self, svg_element, id=None):
        """Animation for all types (Translation, Inflation, Reshape, Opacity)

        Args:
            svg_element (Shape) : The element to animate.
            id          (str)   : An identifier of animation.
        """
        super().__init__(svg_element, id=id)

    def update_angle_translation(self):
        self.update_generic(AnimationType.ANGLE_TRANSLATION, self.svg_el.apply_angle_translation)

    def update(self):
        super().update()
        self.update_angle_translation()
