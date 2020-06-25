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


DEBUG_LEVEL = DebugLevel.NO
DEBUG_LENGTH = max([len(dbg_lvl.name) for dbg_lvl in DebugLevel])

def msg(str, dbg_lvl):
	if DEBUG_LEVEL.value <= dbg_lvl.value:
		print(f"{f'{dbg_lvl.name}'.ljust(DEBUG_LENGTH)} : {str}")

def set_debug(dbg_lvl):
	global DEBUG_LEVEL
	DEBUG_LEVEL = dbg_lvl

