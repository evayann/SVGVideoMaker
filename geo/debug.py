"""
Module who provided the level of debuging.
Useful to display more or less operation of SVGVideoMaker.
"""

# region Imports
from enum import Enum
# endregion Imports

class DebugLevel(Enum):
	VISUAL  = 2  # Add some visual effect on svg element
	VERBOSE = 5  # Tell lot's of information
	WARNING = 7  # Tell only warnings
	NO      = 9  # Quiet like a Carp. Is always the bigger value of enum.

def msg(str, dbg_lvl):
	if DEBUG_LEVEL.value <= dbg_lvl.value:
		print(str)

DEBUG_LEVEL = DebugLevel.NO
