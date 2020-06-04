
# region Imports
from abc import abstractmethod
from enum import Enum
from copy import deepcopy
from geo.shape import Shape
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

class Animation(Shape):

    # Define value for save/get current values of all types
    KEY, VALUES = 0, 1

    def __init__(self, init_point, fps=30, verbose=False,
                 debug=False, id=None, use_style=False, is_fill=False, fill_color="black",
                 is_stroke=False, stroke_color="black", stroke_width=2, opacity=1, others_rules=None):
        super().__init__(debug=debug, id=id, use_style=use_style, is_fill=is_fill, fill_color=fill_color,
                        is_stroke=is_stroke, stroke_color=stroke_color, stroke_width=stroke_width,
                        opacity=opacity, others_rules=others_rules)
        self.fps = fps
        self.current_frame = 0 # Frame number

        self.animations = dict()
        for anim_type in AnimationType:
            self.animations[anim_type] = dict() # Position of element with second in key

        self.animations[AnimationType.MODIFICATION][0] = init_point # Add the init_point for MODIFICATION
        self.animations[AnimationType.DISPLAY][0] = opacity # Add the init display for DISPLAY

        self.anim_computed = None

        self.current_values = dict()
        for anim_type in AnimationType:
            self.current_values[anim_type] = (-1, None) # Initialization

        self.verbose = verbose
        self.nb_frames = 0
        self.end_time = -1

    def set_verbose(self, boolean):
        self.verbose = boolean

    def set_fps(self, fps):
        self.fps = fps

    def init_animation(self):
        self.anim_computed = deepcopy(self.animations)

    def finish_animation(self):
        self.anim_computed = None # Clear element computed

    def add_animation_by_frame(self, frame, values, anim_type=AnimationType.TRANSLATION):
        # Check the data
        # TODO

        # Add data if is good
        self.animations[anim_type][frame] = deepcopy(values) # To don't be affect about possible modification
        self.nb_frames = max(frame, self.nb_frames)

    def update(self):
        """
        Update all animation, modification need to be in first
        :return:
        """
        self.update_translation()
        self.update_inflation()
        self.update_display()
        # Increment frame counter
        self.current_frame += 1

    def read_animation(self, anim_type, force=False):
        """
        Read the animation to compute and return the previous animation values with his key time
        and also the next animations values and his key time
        :param anim_type: the type of animation to read (in AnimationType)
        :param force: oblige to search animation, if false can use element in save memory
        :return: the previous animation values with his key time  and also the next animations values and his key time
        """
        # if self.current_frame >= self.work_anim[anim_type][Animation.CURRENT][Animation.FRAME] or force:
        if self.current_frame >= self.current_values[anim_type][Animation.KEY] or force:
            # Search next animation data
            previous_anim, previous_time = None, 0
            try:
                for key_time, animation in self.anim_computed[anim_type].items():
                    # We pass the value
                    if self.current_frame < key_time:
                        return AnimationState.NEW, (previous_anim, previous_time), (animation, key_time)
                    # Set previous element
                    previous_anim = animation
                    previous_time = key_time
                else:
                    # End of animation
                    return AnimationState.END, (None, 0), (None, 0)
            except StopIteration:
                # No animation for this element
                return AnimationState.END, (None, 0), (None, 0)
        else:  # We have already the next animation data
            return AnimationState.SAME, (None, None), (None, None)

    def update_translation(self):
        state, (_, start_time), (translation, end_time) = self.read_animation(AnimationType.TRANSLATION)
        if state is AnimationState.NEW:
            self.current_values[AnimationType.TRANSLATION] = (end_time, translation / (end_time - start_time))
            self.apply_translation(self.current_values[AnimationType.TRANSLATION][Animation.VALUES])
        elif state is AnimationState.SAME:
            # Send the translation to add
            self.apply_translation(self.current_values[AnimationType.TRANSLATION][Animation.VALUES])

    def update_inflation(self):
        state, (_, start_time), (inflation, end_time) = self.read_animation(AnimationType.INFLATION)
        if state is AnimationState.NEW:
            self.current_values[AnimationType.INFLATION] = (end_time, inflation / (end_time - start_time))
            self.apply_inflation(self.current_values[AnimationType.INFLATION][Animation.VALUES])
        elif state is AnimationState.SAME:
            # Send the inflation to add
            self.apply_inflation(self.current_values[AnimationType.INFLATION][Animation.VALUES])

    def update_display(self):
        state, (old_opacity, start_time), (new_opacity, end_time) = self.read_animation(AnimationType.DISPLAY)
        if state is AnimationState.NEW:
            # Compute and apply opacity
            self.current_values[AnimationType.DISPLAY] = (end_time, (new_opacity - old_opacity) / (end_time - start_time))
            self.opacity = round(self.opacity + self.current_values[AnimationType.DISPLAY][Animation.VALUES], 3)
        elif state is AnimationState.SAME:
            self.opacity = round(self.opacity + self.current_values[AnimationType.DISPLAY][Animation.VALUES], 3)

    def reset(self):
        # Reset frame counter
        self.current_frame = 0

    # region Getters
    def get_end_time(self):
        return self.end_time

    def get_nb_frames(self):
        return self.nb_frames
    # endregion Getters

    def display_animations(self):
        string = f"{self.id}, fps: {self.fps}," \
                 f" End time: {self.end_time}, Nb frames:{self.nb_frames}\n"
        for anim_type in AnimationType:
            string += f"\t{anim_type} : \n"

            # Get the number of digit for a nice format
            nb_key = len(str(self.nb_frames))
            nb_values = len(str(len(self.animations[anim_type].values())))
            have_element = False

            for key, values in self.animations[anim_type].items():
                string += f"\t\t>Frame: {key:{nb_key}},"
                if anim_type is AnimationType.MODIFICATION:
                    string += f"Size:{len(values):{nb_values}}, {str(values)}\n"
                else:
                    string += f"{values}\n"
                have_element = True

            if not have_element:
                string += "\t\t>Empty\n"

        return string

    # region Abstract
    @abstractmethod
    def apply_translation(self, value):
        pass

    @abstractmethod
    def apply_inflation(self, value):
        pass
    # endregion Abstract

    # region Override
    def __str__(self):
        self.display_animations()
    # endregion Override

class ModificationAnimation(Animation):
    def __init__(self, init_point, fps=30, verbose=False,
                 debug=False, use_style=False, is_fill=False, fill_color="black",
                 is_stroke=False, stroke_color="black", stroke_width=2, opacity=1, others_rules=None):
        super().__init__(init_point, fps, verbose, debug=debug, use_style=use_style, is_fill=is_fill, fill_color=fill_color,
                        is_stroke=is_stroke, stroke_color=stroke_color, stroke_width=stroke_width,
                        opacity=opacity, others_rules=others_rules)

    def update_modification(self):
        state, (previous_val, start_frame), (next_val, end_frame) = self.read_animation(AnimationType.MODIFICATION)
        if state is AnimationState.NEW:
            if len(previous_val) != len(next_val):
                if self.verbose:
                    print(f"Not same size between key: {start_frame} and key: {end_frame} !")

                # Simplify writing
                anims = self.anim_computed[AnimationType.MODIFICATION]

                # Not same number of point, need to reshape element before add element
                if len(previous_val) > len(next_val):
                    # Don't need to apply reshape because we have more points than necessary
                    anims[end_frame] = self.reshape(next_val, previous_val)
                else:
                    # Need to apply the reshape because we need more points to match with next values
                    anims[start_frame] = self.reshape(previous_val, next_val, apply=True)

                # Get new values who are reshape
                _, (previous_val, start_frame), (next_val, end_frame) = \
                    self.read_animation(AnimationType.MODIFICATION, force=True)

            # Compute the difference between previous and next position
            nb_frame_to_move = end_frame - start_frame
            computed = [((n - p) / nb_frame_to_move) for n, p in zip(next_val, previous_val)]
            # Save incrementation to add from start to end frame
            self.current_values[AnimationType.MODIFICATION] = (end_frame, computed)
            # Send the modification to add
            self.apply_modification(computed)
        elif state is AnimationState.SAME:
            # Send modification
            self.apply_modification(self.current_values[AnimationType.MODIFICATION][Animation.VALUES])

    def update(self):
        """
        Override default update
        :return:
        """
        # Proceeded
        self.update_modification()
        super().update()

    # region Abstract
    @abstractmethod
    def reshape(self, lower_shape, bigger_shape, apply=False):
        """
        Make a new form for the animation
        The lower form is improve to match to bigger form
        :param lower_shape: the lower_shape of animation
        :param bigger_shape: the bigger_shape of animation
        :param apply: indicate if we need to apply the shape at the form
        :return: an animation who match to bigger_shape from lower_shape
        """
        pass

    @abstractmethod
    def apply_shape(self, shape):
        pass

    @abstractmethod
    def apply_modification(self, values):
        pass
    # endregion Abstract