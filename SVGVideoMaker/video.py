"""
Necessary to make simple video
"""

# region Imports
import os
from enum import Enum
from getpass import getuser
from cairosvg import svg2png
from subprocess import Popen, PIPE
from math import ceil
from SVGVideoMaker.geo.debug import msg, DebugLevel
# endregion Imports

class Format(Enum):
    """
    Enumeration of different format (Picture, Video)
    """
    PNG = "png"
    SVG = "svg"
    MP4 = "mp4"
    GIF = "gif"

class Video:
    """ Instantiate a Video Maker.

    Args:
        svg     (SVG) : the svg to draw
        width   (int) : width in px
        height  (int) : height in px
        fps     (int) : number of frames per seconds
    """
    file_count = 0

    def __init__(self, svg, width=500, height=500, fps=30):
        self.svg = svg

        # Frame per seconds
        self.fps = fps

        # Size / Dimension
        self.width = width
        self.height = height
        self.svg.set_size(width, height)

    def make_movie(self, start=None, end=None):
        """Generator who return all svg in string for each frame.

        Args:
            start (int): Begin of movie in seconds.
            end   (int): End of movie in seconds.

        Yields:
            All svg frames in string with the frame number
        """

        # Prepare the size of movie
        start_frame = ceil(start) * self.fps if start else 0
        end_frame = ceil(end) * self.fps if end else self.svg.get_nb_frames()

        # Inform the different key animation
        msg(self.svg.get_keys_animations(), DebugLevel.VERBOSE)

        # Encapsulate generator in try to reset animation
        # if the generator was break
        try:
            self.svg.init_animation()
            # Around max time to sup value
            for i in range(start_frame, end_frame):
                msg(f"Compute frame {i}", DebugLevel.VERBOSE)
                yield i, self.svg.get_svg()
                self.svg.update()
        except GeneratorExit:
            # Reset animation when generator was break
            self.svg.reset()

        # Normal reset
        self.svg.reset()

    def save_movie(self, start=None, end=None, path="./", name="out", ext="mp4"):
        """Make a video file from svg and all the key frame.

        Args:
            start (int): Begin of movie in seconds.
            end   (int): End of movie in seconds.
            path  (str) : The path where you save video. Default "./".
            name  (str) : The name of video. Default "out".
            ext   (str) : The extension of your video. Default mp4.
        """

        # Prepare command to write video
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output file if exist
            "-s", f"{self.width}x{self.height}",  # Size
            "-r", f"{self.fps}",  # fps
            "-i", "-",  # input come from a pipe like that "exec | ffmpeg"
            "-filter_complex",  # filter to make a higer quality color palette
            "[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse",
            f"{path}{name}.{ext}"
        ]

        pipe = Popen(cmd, stdin=PIPE, stderr=PIPE) # Start video compilation with command
        # Display bytestream on stdin to pass at ffmpeg
        for _, frame in self.make_movie(start, end):
            pipe.stdin.write(svg2png(frame))
        pipe.stdin.close()
        pipe.wait()

    def save_frame(self, frame_number=-1, path="./", name=None):
        """Save the frame 'frame_number' on a file at 'path' with 'name' and extension 'ext'.

        Args:
            frame_number (int) : The number of frame to save if not given save last frame. Default is last frame (-1).
            path         (str) : The path where you save frame. Default path "./".
            name         (str) : The name of your frame. Default random name like "frame_numberXXXXX".
        """

        # Compute name
        if name:
            n = name
        else:
            n = f"frame{frame_number}_{str(Video.file_count).zfill(5)}"
            Video.file_count += 1

        frame = None
        # Find frame and save it
        for i, frame in self.make_movie():
            if i + 1 == frame_number:
                # If no name given, assign name like that : frame_53_00001
                save(frame, f"{path}{n}", Format.SVG)
                break
        else:  # If frame not found, print last
            if frame:
                save(frame, path, Format.PNG)
            else:
                # If None, the movie have no frame
                raise Exception(f"Can't display frame {frame_number} if movie have no frame")

    def print_frame(self, frame_number=-1):
        """Print frame on terminal, if 'frame_number' is -1, print last frame.

        Args:
            frame_number (int) : The number of frame to save. Default -1 save last frame.
        """
        path = get_default_path_name()
        i, frame, max_time = 0, None, self.svg.get_max_time()
        # Find frame and save it on tmp
        for i, frame in self.make_movie():
            if i + 1 == frame_number:
                save(frame, path, Format.PNG)
                break
        else:  # If frame not found, print last frame we have
            if frame:
                save(frame, path, Format.PNG)
                frame_number = i # Change the number of frame
            else:
                # If None, the movie have no frame
                raise Exception(f"Can't display frame {frame_number} if movie have no frame")

        display_on_term(f"{path}", f"Frame {frame_number}" if frame_number != -1 else "Last frame")

# region Utility
def get_default_path_name(ext=Format.PNG):
    """Get a string who indicate a default path with a default name

    Args:
        ext (Format or str) : The extension to add at end of path name. Default "png".

    Returns:
        The string to indicate default path.
    """
    # Create different directories for each user
    path = f"/tmp/{getuser()}/"
    if not os.path.exists(path):
        os.makedirs(path)

    ext = ext.value if isinstance(ext, Format) else ext
    path_name = f"{path}svg_frame{str(Video.file_count).zfill(5)}.{ext}"
    Video.file_count += 1
    return path_name

def save(element, path, ext):
    """Save element at path with extension 'ext'.

    Args:
        element (str)           : The element to save.
        path    (str)           : The path to save element.
        ext     (Format or str) : The extension for element.
    """
    ext = ext.value if isinstance(ext, Format) else ext
    if ext == Format.PNG.value:
        svg2png(element, write_to=f"{path}.{ext}")
    elif ext == Format.SVG.value:
        with open(f"{path}.{ext}", "w") as f:
            f.write(element)
            f.close()
# endregion Utility

# region Terminal
def display(svg_element, path=None, name=None, ext=Format.PNG):
    """Display the svg on terminal, if no name or path, save it in default path and name.

    Args:
        svg_element (Shape)         : The element to display.
        path        (str)           : The path to save element. Default path.
        name        (str)           : The name of file. Default name.
        ext         (Format or str) : The extension of element (SVG or PNG). Default "png".
    """
    extension = ext.value if isinstance(ext, Format) else ext
    path = f"{path}{name}.{extension}" if path and name else get_default_path_name(ext)
    save(svg_element.get_svg(), path, ext)
    display_on_term(path, f"{name}" if name else f"{path}")

def display_on_term(path_to_file, title=None):
    """Display picture save at path_to_file. Add title if not None before picture.

    Args:
        path_to_file: The path of picture.
        title: The title to display. If title print it on terminal.
    """
    if title:
        print(f"{title}")
    try:
        # Search if we can display picture in the terminal
        # And display it if it's possible
        terminal = os.environ["TERM"]
        if terminal == "xterm-kitty":
            os.system(f"kitty +kitten icat {path_to_file}")
        elif terminal == "terminolgy":
            os.system(f"tycat {path_to_file}")
        elif terminal == "xterm-256color":
            print("Not supported natively")
            os.system(f"viu {path_to_file}")
            print(f"If you don't see image, "
                  f"You can display pseudo image in {terminal} "
                  f"By installing viu (command cargo install viu), who need rust.")
        else:
            print(f"Terminal {terminal} isn't supported")
    except KeyError:
        # If we don't in a terminal, we can't get os.environ["TERM"]
        print("Not in terminal")
# endregion Terminal
