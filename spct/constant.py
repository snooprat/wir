import curses
from typing import Union


# CONSTANT

# Type
T_COLOR = Union[str, int]

# Text attributes for printing the screen.
A_BLINK = curses.A_BLINK
A_BOLD = curses.A_BOLD
A_DIM = curses.A_DIM
A_INVIS = curses.A_INVIS
A_NORMAL = curses.A_NORMAL
A_REVERSE = curses.A_REVERSE
A_STANDOUT = curses.A_STANDOUT
A_UNDERLINE = curses.A_UNDERLINE

# Text extract attributes for get properties.
A_ATTRIBUTES = curses.A_ATTRIBUTES
A_CHARTEXT = curses.A_CHARTEXT
A_COLOR = curses.A_COLOR

# Text align attributes.
A_TOP = 1
A_MIDDLE = 2
A_BOTTOM = 3
A_LEFT = 4
A_CENTER = 5
A_RIGHT = 6

# Text colors for printing the screen.
COLOR_BLACK = curses.COLOR_BLACK
COLOR_BLUE = curses.COLOR_BLUE
COLOR_CYAN = curses.COLOR_CYAN
COLOR_GREEN = curses.COLOR_GREEN
COLOR_MAGENTA = curses.COLOR_MAGENTA
COLOR_RED = curses.COLOR_RED
COLOR_WHITE = curses.COLOR_WHITE
COLOR_YELLOW = curses.COLOR_YELLOW

# Standard extended key codes.
KEY_MIN = curses.KEY_MIN
KEY_BREAK = curses.KEY_BREAK
KEY_SRESET = curses.KEY_SRESET
KEY_RESET = curses.KEY_RESET
KEY_DOWN = curses.KEY_DOWN
KEY_UP = curses.KEY_UP
KEY_LEFT = curses.KEY_LEFT
KEY_RIGHT = curses.KEY_RIGHT
KEY_HOME = curses.KEY_HOME
KEY_BACKSPACE = curses.KEY_BACKSPACE
KEY_F0 = curses.KEY_F0
KEY_F1 = curses.KEY_F1
KEY_F2 = curses.KEY_F2
KEY_F3 = curses.KEY_F3
KEY_F4 = curses.KEY_F4
KEY_F5 = curses.KEY_F5
KEY_F6 = curses.KEY_F6
KEY_F7 = curses.KEY_F7
KEY_F8 = curses.KEY_F8
KEY_F9 = curses.KEY_F9
KEY_F10 = curses.KEY_F10
KEY_F11 = curses.KEY_F11
KEY_F12 = curses.KEY_F12
KEY_DL = curses.KEY_DL
KEY_IL = curses.KEY_IL
KEY_DC = curses.KEY_DC
KEY_IC = curses.KEY_IC
KEY_EIC = curses.KEY_EIC
KEY_CLEAR = curses.KEY_CLEAR
KEY_EOS = curses.KEY_EOS
KEY_EOL = curses.KEY_EOL
KEY_SF = curses.KEY_SF
KEY_SR = curses.KEY_SR
KEY_NPAGE = curses.KEY_NPAGE
KEY_PPAGE = curses.KEY_PPAGE
KEY_STAB = curses.KEY_STAB
KEY_CTAB = curses.KEY_CTAB
KEY_CATAB = curses.KEY_CATAB
KEY_ENTER = curses.KEY_ENTER
KEY_PRINT = curses.KEY_PRINT
KEY_LL = curses.KEY_LL
KEY_A1 = curses.KEY_A1
KEY_A3 = curses.KEY_A3
KEY_B2 = curses.KEY_B2
KEY_C1 = curses.KEY_C1
KEY_C3 = curses.KEY_C3
KEY_BTAB = curses.KEY_BTAB
KEY_BEG = curses.KEY_BEG
KEY_CANCEL = curses.KEY_CANCEL
KEY_CLOSE = curses.KEY_CLOSE
KEY_COMMAND = curses.KEY_COMMAND
KEY_COPY = curses.KEY_COPY
KEY_CREATE = curses.KEY_CREATE
KEY_END = curses.KEY_END
KEY_EXIT = curses.KEY_EXIT
KEY_FIND = curses.KEY_FIND
KEY_HELP = curses.KEY_HELP
KEY_MARK = curses.KEY_MARK
KEY_MESSAGE = curses.KEY_MESSAGE
KEY_MOVE = curses.KEY_MOVE
KEY_NEXT = curses.KEY_NEXT
KEY_OPEN = curses.KEY_OPEN
KEY_OPTIONS = curses.KEY_OPTIONS
KEY_PREVIOUS = curses.KEY_PREVIOUS
KEY_REDO = curses.KEY_REDO
KEY_REFERENCE = curses.KEY_REFERENCE
KEY_REFRESH = curses.KEY_REFRESH
KEY_REPLACE = curses.KEY_REPLACE
KEY_RESTART = curses.KEY_RESTART
KEY_RESUME = curses.KEY_RESUME
KEY_SAVE = curses.KEY_SAVE
KEY_SBEG = curses.KEY_SBEG
KEY_SCANCEL = curses.KEY_SCANCEL
KEY_SCOMMAND = curses.KEY_SCOMMAND
KEY_SCOPY = curses.KEY_SCOPY
KEY_SCREATE = curses.KEY_SCREATE
KEY_SDC = curses.KEY_SDC
KEY_SDL = curses.KEY_SDL
KEY_SELECT = curses.KEY_SELECT
KEY_SEND = curses.KEY_SEND
KEY_SEOL = curses.KEY_SEOL
KEY_SEXIT = curses.KEY_SEXIT
KEY_SFIND = curses.KEY_SFIND
KEY_SHELP = curses.KEY_SHELP
KEY_SHOME = curses.KEY_SHOME
KEY_SIC = curses.KEY_SIC
KEY_SLEFT = curses.KEY_SLEFT
KEY_SMESSAGE = curses.KEY_SMESSAGE
KEY_SMOVE = curses.KEY_SMOVE
KEY_SNEXT = curses.KEY_SNEXT
KEY_SOPTIONS = curses.KEY_SOPTIONS
KEY_SPREVIOUS = curses.KEY_SPREVIOUS
KEY_SPRINT = curses.KEY_SPRINT
KEY_SREDO = curses.KEY_SREDO
KEY_SREPLACE = curses.KEY_SREPLACE
KEY_SRIGHT = curses.KEY_SRIGHT
KEY_SRSUME = curses.KEY_SRSUME
KEY_SSAVE = curses.KEY_SSAVE
KEY_SSUSPEND = curses.KEY_SSUSPEND
KEY_SUNDO = curses.KEY_SUNDO
KEY_SUSPEND = curses.KEY_SUSPEND
KEY_UNDO = curses.KEY_UNDO
KEY_MOUSE = curses.KEY_MOUSE
KEY_RESIZE = curses.KEY_RESIZE
KEY_MAX = curses.KEY_MAX

# Special characters.
C_HIGHLIGHT = '`'

# Symbols
S_A_BLINK = 'A_BLINK'
S_A_BOLD = 'A_BOLD'
S_A_DIM = 'A_DIM'
S_A_INVIS = 'A_INVIS'
S_A_NORMAL = 'A_NORMAL'
S_A_REVERSE = 'A_REVERSE'
S_A_STANDOUT = 'A_STANDOUT'
S_A_UNDERLINE = 'A_UNDERLINE'
S_COLOR_ERROR = -1
S_COLOR_DEFAULT = 'default'
S_COLOR_FG = 'fg'
S_COLOR_BG = 'bg'
S_COLOR_ATTR = 'attr'
S_MAP_MAPH = 'map_height'
S_MAP_MAPW = 'map_width'
S_MAP_MAP = 'map'
S_MAP_CELL = 'cell'
S_MAP_CHAR = 'char'
S_MAP_COLOR = 'color'
S_MAP_GRID_TYPE = 'grid_type'
S_MAP_GRIDH = 'grid_height'
S_MAP_GRIDW = 'grid_width'
S_MAP_GRID_LEN = 'grid_len'
S_MAP_GRID_OFFSET = 'grid_offset'
S_MAP_GRID_SPACE = 'grid_space'
S_MAP_MARGIN = 'map_margin'
S_MAP_GRIDY = 'grid_starty'
S_MAP_GRIDX = 'grid_startx'
S_UPDATE_ALL = -1
S_UPDATE_NONE = -2

# Default Value
DEF_MAP_GRID_LEN = 3
DEF_MAP_GRID_OFFSET = 2
DEF_MAP_GRID_SPACE = 1
DEF_MAP_GRIDY = 0
DEF_MAP_GRIDX = 0
