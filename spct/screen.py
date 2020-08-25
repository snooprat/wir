import sys
import curses
import curses.panel as cpanel


# CONSTANT

# Text attributes for printing the screen.
A_BOLD = curses.A_BOLD
A_NORMAL = curses.A_NORMAL
A_REVERSE = curses.A_REVERSE
A_UNDERLINE = curses.A_UNDERLINE

# Text extract attributes for get properties.
A_ATTRIBUTES = curses.A_ATTRIBUTES
A_CHARTEXT = curses.A_CHARTEXT
A_COLOR = curses.A_COLOR

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

# Text align attributes.
AL_TOP = 1
AL_MIDDLE = 2
AL_BOTTOM = 3
AL_LEFT = 4
AL_CENTER = 5
AL_RIGHT = 6

# Special character for print specific text.
CH_HIGHLIGHT = '`'


class ColorMap(object):
    """Manage colors"""

    def __init__(self, colors=None):
        self._cid = 1
        self._colors = {}
        self._attr = {
            'A_BOLD': A_BOLD,
            'A_NORMAL': A_NORMAL,
            'A_REVERSE': A_REVERSE,
            'A_UNDERLINE': A_UNDERLINE
        }
        self.add_color('default')
        self.add_color_map(colors)

    def add_color(self, sel, fg=COLOR_WHITE, bg=COLOR_BLACK, attr=A_NORMAL):
        curses.init_pair(self._cid, fg, bg)
        self._colors[sel] = curses.color_pair(self._cid) | attr
        self._cid += 1
        return self._colors[sel]

    def add_color_map(self, colors):
        if colors:
            for k, v in colors.items():
                fg = v.get('fg', COLOR_WHITE)
                bg = v.get('bg', COLOR_BLACK)
                attr = self.get_attr(v.get('attr'))
                self.add_color(k, fg, bg, attr)

    def get_attr(self, attr):
        return self._attr.get(attr, A_NORMAL)

    def get_color(self, sel='default'):
        return self._colors.get(sel, self._colors['default'])


def update():
    """Update screen display"""
    cpanel.update_panels()
    curses.doupdate()


def run():
    """Run the top layout's function."""
    while True:
        try:
            top_layout = cpanel.top_panel().userptr()
        except AttributeError:
            sys.exit("Please create at least one view layout.")
        top_layout.run_ctr()


def init():
    curses.curs_set(0)


def wrapper(*args, **kwds):
    curses.wrapper(*args, **kwds)
