
# region Imports
from enum import Enum
from copy import deepcopy
from geo.debug import msg, DebugLevel
# endregion Imports


class AnimationType(Enum):
    """
    Enumeration of different type of animation.
    """
    TRANSLATION = 1
    MODIFICATION = 2
    INFLATION = 3
    DISPLAY = 4

class AnimationState(Enum):
    """
    Enumeration of different state of animation.
    """
    NEW = 0
    SAME = 1
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

    def set_start(self, init_point, opacity):
        self.anims[AnimationType.MODIFICATION][0] = init_point # Add the init_point for MODIFICATION
        self.anims[AnimationType.DISPLAY][0] = opacity # Add the init display for DISPLAY

    def init_animation(self):
        self.anim_computed = deepcopy(self.anims)

    def finish_animation(self):
        self.anim_computed = None # Clear element computed

    def add_animation_by_frame(self, frame, values, anim_type=AnimationType.TRANSLATION):
        # Check the data
        # TODO

        # Add data if is good
        self.anims[anim_type][frame] = deepcopy(values) # To don't be affect about possible modification
        self.nb_frames = max(frame, self.nb_frames)

    def update(self):
        """
        Update all animation, modification need to be in first.
        """
        self.update_translation()
        self.update_inflation()
        self.update_display()
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
        if self.current_frame >= self.current_values[anim_type][Animation.KEY] or force:
            # Search next animation data
            previous_anim, previous_frame = None, 0
            try:
                for key_frame, animation in self.anim_computed[anim_type].items():
                    # We pass the value
                    if self.current_frame < key_frame:
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
            return AnimationState.SAME, (None, None), (None, None)

    def update_translation(self):
        state, (_, start_frame), (translation, end_frame) = self.read_animation(AnimationType.TRANSLATION)
        if state is AnimationState.NEW:
            self.current_values[AnimationType.TRANSLATION] = (end_frame, translation / (end_frame - start_frame))
            self.svg_el.apply_translation(self.current_values[AnimationType.TRANSLATION][Animation.VALUES])
        elif state is AnimationState.SAME:
            # Send the translation to add
            self.svg_el.apply_translation(self.current_values[AnimationType.TRANSLATION][Animation.VALUES])

    def update_inflation(self):
        state, (_, start_frame), (inflation, end_frame) = self.read_animation(AnimationType.INFLATION)
        if state is AnimationState.NEW:
            self.current_values[AnimationType.INFLATION] = (end_frame, inflation / (end_frame - start_frame))
            self.svg_el.apply_inflation(self.current_values[AnimationType.INFLATION][Animation.VALUES])
        elif state is AnimationState.SAME:
            # Send the inflation to add
            self.svg_el.apply_inflation(self.current_values[AnimationType.INFLATION][Animation.VALUES])

    def update_display(self):
        state, (old_opacity, start_frame), (new_opacity, end_frame) = self.read_animation(AnimationType.DISPLAY)
        if state is AnimationState.NEW:
            # Compute and apply opacity
            self.current_values[AnimationType.DISPLAY] = (end_frame, (new_opacity - old_opacity) / (end_frame - start_frame))
            self.svg_el.apply_opacity(self.current_values[AnimationType.DISPLAY][Animation.VALUES])
        elif state is AnimationState.SAME:
            self.svg_el.apply_opacity(self.current_values[AnimationType.DISPLAY][Animation.VALUES])

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
            self.current_values[AnimationType.MODIFICATION] = (end_frame, computed)
            # Send the modification to add
            self.svg_el.apply_modification(computed)
        elif state is AnimationState.SAME:
            # Send modification
            self.svg_el.apply_modification(self.current_values[AnimationType.MODIFICATION][Animation.VALUES])

    def update(self):
        """
        Override update of Animation
        """
        # Proceeded
        self.update_modification()
        super().update()
