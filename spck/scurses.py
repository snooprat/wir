# scurses make unicurses more python native.

import spck.unicurses as uc

# +++ CONSTANTS +++

# Attributes
A_ALTCHARSET = uc.A_ALTCHARSET
A_BLINK = uc.A_BLINK
A_BOLD = uc.A_BOLD
A_DIM = uc.A_DIM
A_NORMAL = uc.A_NORMAL
A_STANDOUT = uc.A_STANDOUT
A_UNDERLINE = uc.A_UNDERLINE
A_REVERSE = uc.A_REVERSE
A_PROTECT = uc.A_PROTECT
A_ATTRIBUTES = uc.A_ATTRIBUTES
A_INVIS = uc.A_INVIS
A_COLOR = uc.A_COLOR
A_CHARTEXT = uc.A_CHARTEXT

# Colors
COLOR_BLACK = uc.COLOR_BLACK
COLOR_BLUE = uc.COLOR_BLUE
COLOR_CYAN = uc.COLOR_CYAN
COLOR_GREEN = uc.COLOR_GREEN
COLOR_MAGENTA = uc.COLOR_MAGENTA
COLOR_RED = uc.COLOR_RED
COLOR_WHITE = uc.COLOR_WHITE
COLOR_YELLOW = uc.COLOR_YELLOW

# ACS Alternate Character Set Symbols
ACS_ULCORNER = uc.ACS_ULCORNER
ACS_LLCORNER = uc.ACS_LLCORNER
ACS_URCORNER = uc.ACS_URCORNER
ACS_LRCORNER = uc.ACS_LRCORNER
ACS_LTEE = uc.ACS_LTEE
ACS_RTEE = uc.ACS_RTEE
ACS_BTEE = uc.ACS_BTEE
ACS_TTEE = uc.ACS_TTEE
ACS_HLINE = uc.ACS_HLINE
ACS_VLINE = uc.ACS_VLINE
ACS_PLUS = uc.ACS_PLUS
ACS_S1 = uc.ACS_S1
ACS_S9 = uc.ACS_S9
ACS_DIAMOND = uc.ACS_DIAMOND
ACS_CKBOARD = uc.ACS_CKBOARD
ACS_DEGREE = uc.ACS_DEGREE
ACS_PLMINUS = uc.ACS_PLMINUS
ACS_BULLET = uc.ACS_BULLET
ACS_LARROW = uc.ACS_LARROW
ACS_RARROW = uc.ACS_RARROW
ACS_DARROW = uc.ACS_DARROW
ACS_UARROW = uc.ACS_UARROW
ACS_BOARD = uc.ACS_BOARD
ACS_LANTERN = uc.ACS_LANTERN
ACS_BLOCK = uc.ACS_BLOCK
ACS_S3 = uc.ACS_S3
ACS_S7 = uc.ACS_S7
ACS_LEQUAL = uc.ACS_LEQUAL
ACS_GEQUAL = uc.ACS_GEQUAL
ACS_PI = uc.ACS_PI
ACS_NEQUAL = uc.ACS_NEQUAL
ACS_STERLING = uc.ACS_STERLING
ACS_BSSB = ACS_ULCORNER
ACS_SSBB = ACS_LLCORNER
ACS_BBSS = ACS_URCORNER
ACS_SBBS = ACS_LRCORNER
ACS_SBSS = ACS_RTEE
ACS_SSSB = ACS_LTEE
ACS_SSBS = ACS_BTEE
ACS_BSSS = ACS_TTEE
ACS_BSBS = ACS_HLINE
ACS_SBSB = ACS_VLINE
ACS_SSSS = ACS_PLUS

# Keymap
# KEY_CODE_YES = uc.KEY_CODE_YES
KEY_MIN = uc.KEY_MIN
KEY_BREAK = uc.KEY_BREAK
KEY_SRESET = uc.KEY_SRESET
KEY_RESET = uc.KEY_RESET
KEY_DOWN = uc.KEY_DOWN
KEY_UP = uc.KEY_UP
KEY_LEFT = uc.KEY_LEFT
KEY_RIGHT = uc.KEY_RIGHT
KEY_HOME = uc.KEY_HOME
KEY_BACKSPACE = uc.KEY_BACKSPACE
KEY_F0 = uc.KEY_F0
KEY_DL = uc.KEY_DL
KEY_IL = uc.KEY_IL
KEY_DC = uc.KEY_DC
KEY_IC = uc.KEY_IC
KEY_EIC = uc.KEY_EIC
KEY_CLEAR = uc.KEY_CLEAR
KEY_EOS = uc.KEY_EOS
KEY_EOL = uc.KEY_EOL
KEY_SF = uc.KEY_SF
KEY_SR = uc.KEY_SR
KEY_NPAGE = uc.KEY_NPAGE
KEY_PPAGE = uc.KEY_PPAGE
KEY_STAB = uc.KEY_STAB
KEY_CTAB = uc.KEY_CTAB
KEY_CATAB = uc.KEY_CATAB
KEY_ENTER = uc.KEY_ENTER
KEY_PRINT = uc.KEY_PRINT
KEY_LL = uc.KEY_LL
KEY_A1 = uc.KEY_A1
KEY_A3 = uc.KEY_A3
KEY_B2 = uc.KEY_B2
KEY_C1 = uc.KEY_C1
KEY_C3 = uc.KEY_C3
KEY_BTAB = uc.KEY_BTAB
KEY_BEG = uc.KEY_BEG
KEY_CANCEL = uc.KEY_CANCEL
KEY_CLOSE = uc.KEY_CLOSE
KEY_COMMAND = uc.KEY_COMMAND
KEY_COPY = uc.KEY_COPY
KEY_CREATE = uc.KEY_CREATE
KEY_END = uc.KEY_END
KEY_EXIT = uc.KEY_EXIT
KEY_FIND = uc.KEY_FIND
KEY_HELP = uc.KEY_HELP
KEY_MARK = uc.KEY_MARK
KEY_MESSAGE = uc.KEY_MESSAGE
KEY_MOVE = uc.KEY_MOVE
KEY_NEXT = uc.KEY_NEXT
KEY_OPEN = uc.KEY_OPEN
KEY_OPTIONS = uc.KEY_OPTIONS
KEY_PREVIOUS = uc.KEY_PREVIOUS
KEY_REDO = uc.KEY_REDO
KEY_REFERENCE = uc.KEY_REFERENCE
KEY_REFRESH = uc.KEY_REFRESH
KEY_REPLACE = uc.KEY_REPLACE
KEY_RESTART = uc.KEY_RESTART
KEY_RESUME = uc.KEY_RESUME
KEY_SAVE = uc.KEY_SAVE
KEY_SBEG = uc.KEY_SBEG
KEY_SCANCEL = uc.KEY_SCANCEL
KEY_SCOMMAND = uc.KEY_SCOMMAND
KEY_SCOPY = uc.KEY_SCOPY
KEY_SCREATE = uc.KEY_SCREATE
KEY_SDC = uc.KEY_SDC
KEY_SDL = uc.KEY_SDL
KEY_SELECT = uc.KEY_SELECT
KEY_SEND = uc.KEY_SEND
KEY_SEOL = uc.KEY_SEOL
KEY_SEXIT = uc.KEY_SEXIT
KEY_SFIND = uc.KEY_SFIND
KEY_SHELP = uc.KEY_SHELP
KEY_SHOME = uc.KEY_SHOME
KEY_SIC = uc.KEY_SIC
KEY_SLEFT = uc.KEY_SLEFT
KEY_SMESSAGE = uc.KEY_SMESSAGE
KEY_SMOVE = uc.KEY_SMOVE
KEY_SNEXT = uc.KEY_SNEXT
KEY_SOPTIONS = uc.KEY_SOPTIONS
KEY_SPREVIOUS = uc.KEY_SPREVIOUS
KEY_SPRINT = uc.KEY_SPRINT
KEY_SREDO = uc.KEY_SREDO
KEY_SREPLACE = uc.KEY_SREPLACE
KEY_SRIGHT = uc.KEY_SRIGHT
KEY_SRSUME = uc.KEY_SRSUME
KEY_SSAVE = uc.KEY_SSAVE
KEY_SSUSPEND = uc.KEY_SSUSPEND
KEY_SUNDO = uc.KEY_SUNDO
KEY_SUSPEND = uc.KEY_SUSPEND
KEY_UNDO = uc.KEY_UNDO
KEY_MOUSE = uc.KEY_MOUSE
KEY_RESIZE = uc.KEY_RESIZE
# KEY_EVENT = curses.KEY_EVENT
KEY_MAX = uc.KEY_MAX

# Mouse mapping
BUTTON1_RELEASED = uc.BUTTON1_RELEASED
BUTTON1_PRESSED = uc.BUTTON1_PRESSED
BUTTON1_CLICKED = uc.BUTTON1_CLICKED
BUTTON1_DOUBLE_CLICKED = uc.BUTTON1_DOUBLE_CLICKED
BUTTON1_TRIPLE_CLICKED = uc.BUTTON1_TRIPLE_CLICKED

BUTTON2_RELEASED = uc.BUTTON2_RELEASED
BUTTON2_PRESSED = uc.BUTTON2_PRESSED
BUTTON2_CLICKED = uc.BUTTON2_CLICKED
BUTTON2_DOUBLE_CLICKED = uc.BUTTON2_DOUBLE_CLICKED
BUTTON2_TRIPLE_CLICKED = uc.BUTTON2_TRIPLE_CLICKED

BUTTON3_RELEASED = uc.BUTTON3_RELEASED
BUTTON3_PRESSED = uc.BUTTON3_PRESSED
BUTTON3_CLICKED = uc.BUTTON3_CLICKED
BUTTON3_DOUBLE_CLICKED = uc.BUTTON3_DOUBLE_CLICKED
BUTTON3_TRIPLE_CLICKED = uc.BUTTON3_TRIPLE_CLICKED

BUTTON4_RELEASED = uc.BUTTON4_RELEASED
BUTTON4_PRESSED = uc.BUTTON4_PRESSED
BUTTON4_CLICKED = uc.BUTTON4_CLICKED
BUTTON4_DOUBLE_CLICKED = uc.BUTTON4_DOUBLE_CLICKED
BUTTON4_TRIPLE_CLICKED = uc.BUTTON4_TRIPLE_CLICKED

BUTTON_SHIFT = uc.BUTTON_SHIFT
BUTTON_CTRL = uc.BUTTON_CTRL
BUTTON_ALT = uc.BUTTON_ALT

ALL_MOUSE_EVENTS = uc.ALL_MOUSE_EVENTS
REPORT_MOUSE_POSITION = uc.REPORT_MOUSE_POSITION

# --- CONSTANTS ---


# +++ FUNCTIONS +++

# Curses functions
baudrate = uc.baudrate
beep = uc.beep
can_change_color = uc.can_change_color
cbreak = uc.cbreak
color_content = uc.color_content
color_pair = uc.color_pair
curs_set = uc.curs_set
def_prog_mode = uc.def_prog_mode
def_shell_mode = uc.def_shell_mode
delay_output = uc.delay_output
doupdate = uc.doupdate
echo = uc.echo
endwin = uc.endwin
erasechar = uc.erasechar
filter = uc.filter
flash = uc.flash
flushinp = uc.flushinp
halfdelay = uc.halfdelay
has_colors = uc.has_colors
has_ic = uc.has_ic
has_il = uc.has_il
has_key = uc.has_key
init_color = uc.init_color
init_pair = uc.init_pair
isendwin = uc.isendwin
keyname = uc.keyname
killchar = uc.killchar
longname = uc.longname
mouseinterval = uc.mouseinterval
mousemask = uc.mousemask
napms = uc.napms
nl = uc.nl
nocbreak = uc.nocbreak
nodelay = uc.nodelay
noecho = uc.noecho
nonl = uc.nonl
noqiflush = uc.noqiflush
noraw = uc.noraw
pair_content = uc.pair_content
pair_number = uc.pair_number
putp = uc.putp
qiflush = uc.qiflush
raw = uc.raw
reset_prog_mode = uc.reset_prog_mode
reset_shell_mode = uc.reset_shell_mode
setsyx = uc.setsyx
setupterm = uc.setupterm
start_color = uc.start_color
termattrs = uc.termattrs
termname = uc.termname
tigetflag = uc.tigetflag
tigetnum = uc.tigetnum
tigetstr = uc.tigetstr
tparm = uc.tparm
typeahead = uc.typeahead
unctrl = uc.unctrl
ungetch = uc.ungetch
ungetmouse = uc.ungetmouse
untouchwin = uc.untouchwin
use_default_colors = uc.use_default_colors
use_env = uc.use_env


# Functions based on window object
class WinObj(object):
    """window object from curses."""

    def __init__(self, scr):
        self.scr = scr

    def __del__(self):
        return uc.delwin(self.scr)

    def _overload(self, args, kwds, num, func1, func2):
        """overload function by number of args"""
        if len(args) + len(kwds) <= num:
            return func1(self.scr, *args, **kwds)
        else:
            return func2(self.scr, *args, **kwds)

    def addch(self, *args, **kwds):
        return self._overload(args, kwds, 2, uc.waddch, uc.mvwaddch)

    def addstr(self, *args, **kwds):
        return self._overload(args, kwds, 2, uc.waddstr, uc.mvwaddstr)

    def addnstr(self, *args, **kwds):
        return self._overload(args, kwds, 3, uc.waddnstr, uc.mvwaddnstr)

    def attroff(self, *args, **kwds):
        return uc.wattroff(self.scr, *args, **kwds)

    def attron(self, *args, **kwds):
        return uc.wattron(self.scr, *args, **kwds)

    def bkgd(self, *args, **kwds):
        return uc.wbkgd(self.scr, *args, **kwds)

    def bkgdset(self, *args, **kwds):
        return uc.wbkgdset(self.scr, *args, **kwds)

    def border(self, *args, **kwds):
        return uc.wborder(self.scr, *args, **kwds)

    def box(self, *args, **kwds):
        return uc.box(self.scr, *args, **kwds)

    def chgat(self, *args, **kwds):
        return self._overload(args, kwds, 4, uc.wchgat, uc.mvwchgat)

    def clear(self, *args, **kwds):
        return uc.wclear(self.scr, *args, **kwds)

    def clrtobot(self, *args, **kwds):
        return uc.wclrtobot(self.scr, *args, **kwds)

    def clrtoeol(self, *args, **kwds):
        return uc.wclrtoeol(self.scr, *args, **kwds)

    def clearok(self, *args, **kwds):
        return uc.clearok(self.scr, *args, **kwds)

    def cursyncup(self, *args, **kwds):
        return uc.wcursyncup(self.scr, *args, **kwds)

    def delch(self, *args, **kwds):
        return self._overload(args, kwds, 0, uc.wdelch, uc.mvwdelch)

    def deleteln(self, *args, **kwds):
        return self._overload(args, kwds, 0, uc.wdeleteln, uc.mvwdeleteln)

    def _dw_2args(self, begin_y, begin_x):
        ml, mc = self.getmaxyx()
        nl = ml - begin_y
        nc = mc - begin_x
        return WinObj(uc.derwin(self.scr, nl, nc, begin_y, begin_x))

    def derwin(self, *args, **kwds):
        if len(args) + len(kwds) <= 2:
            return self._dw_2args(*args, **kwds)
        else:
            return WinObj(uc.derwin(self.scr, *args, **kwds))

    def echochar(self, *args, **kwds):
        return uc.wechochar(self.scr, *args, **kwds)

    def enclose(self, *args, **kwds):
        return uc.enclose(self.scr, *args, **kwds)

    def erase(self, *args, **kwds):
        return uc.werase(self.scr, *args, **kwds)

    def getbegyx(self, *args, **kwds):
        return uc.getbegyx(self.scr, *args, **kwds)

    def getch(self, *args, **kwds):
        return self._overload(args, kwds, 0, uc.wgetch, uc.mvwgetch)

    def getkey(self, *args, **kwds):
        return uc.wgetkey(self.scr, *args, **kwds)

    def getmaxyx(self, *args, **kwds):
        return uc.getmaxyx(self.scr, *args, **kwds)

    def getmouse(self, *args, **kwds):
        return uc.getmouse(self.scr, *args, **kwds)

    def getparyx(self, *args, **kwds):
        return uc.getparyx(self.scr, *args, **kwds)

    def getstr(self, *args, **kwds):
        return self._overload(args, kwds, 0, uc.wgetstr, uc.mvwgetstr)

    def getsyx(self, *args, **kwds):
        return uc.getsyx(self.scr, *args, **kwds)

    def getwin(self, *args, **kwds):
        return uc.getwin(self.scr, *args, **kwds)

    def getyx(self, *args, **kwds):
        return uc.getyx(self.scr, *args, **kwds)

    def hline(self, *args, **kwds):
        return self._overload(args, kwds, 2, uc.whline, uc.mvwhline)

    def idcok(self, *args, **kwds):
        return uc.idcok(self.scr, *args, **kwds)

    def idlok(self, *args, **kwds):
        return uc.idlok(self.scr, *args, **kwds)

    def immedok(self, *args, **kwds):
        return uc.immedok(self.scr, *args, **kwds)

    def inch(self, *args, **kwds):
        return self._overload(args, kwds, 0, uc.winch, uc.mvwinch)

    def insch(self, *args, **kwds):
        return self._overload(args, kwds, 2, uc.winsch, uc.mvwinsch)

    def insdelln(self, *args, **kwds):
        return uc.winsdelln(self.scr, *args, **kwds)

    def insstr(self, *args, **kwds):
        return self._overload(args, kwds, 2, uc.winsstr, uc.mvwinsstr)

    def insnstr(self, *args, **kwds):
        return self._overload(args, kwds, 3, uc.winsnstr, uc.mvwinsnstr)

    def instr(self, *args, **kwds):
        return self._overload(args, kwds, 1, uc.winstr, uc.mvwinstr)

    def insertln(self, *args, **kwds):
        return uc.winsertln(self.scr, *args, **kwds)

    def is_linetouched(self, *args, **kwds):
        return uc.is_linetouched(self.scr, *args, **kwds)

    def is_wintouched(self, *args, **kwds):
        return uc.is_wintouched(self.scr, *args, **kwds)

    def keypad(self, *args, **kwds):
        return uc.keypad(self.scr, *args, **kwds)

    def leaveok(self, *args, **kwds):
        return uc.leaveok(self.scr, *args, **kwds)

    def meta(self, *args, **kwds):
        return uc.meta(self.scr, *args, **kwds)

    def move(self, *args, **kwds):
        return uc.wmove(self.scr, *args, **kwds)

    def mvderwin(self, *args, **kwds):
        return uc.mvderwin(self.scr, *args, **kwds)

    def mvwin(self, *args, **kwds):
        return uc.mvwin(self.scr, *args, **kwds)

    def notimeout(self, *args, **kwds):
        return uc.notimeout(self.scr, *args, **kwds)

    def noutrefresh(self, *args, **kwds):
        return uc.noutrefresh(self.scr, *args, **kwds)

    def _ol_1args(self, destwin):
        return uc.overlay(self.scr, destwin.scr)

    def _ol_7args(self, destwin, sminrow, smincol, dminrow, dmincol, dmaxrow,
                  dmaxcol):
        return uc.copywin(self.scr, destwin.scr, sminrow, smincol, dminrow,
                          dmincol, dmaxrow, dmaxcol, True)

    def overlay(self, *args, **kwds):
        if len(args) + len(kwds) <= 1:
            return self._ol_1args(*args, **kwds)
        else:
            return self._ol_7args(*args, **kwds)

    def _ow_1args(self, destwin):
        return uc.overwrite(self.scr, destwin.scr)

    def _ow_7args(self, destwin, sminrow, smincol, dminrow, dmincol, dmaxrow,
                  dmaxcol):
        return uc.copywin(self.scr, destwin.scr, sminrow, smincol, dminrow,
                          dmincol, dmaxrow, dmaxcol, False)

    def overwrite(self, *args, **kwds):
        if len(args) + len(kwds) <= 1:
            return self._ow_1args(*args, **kwds)
        else:
            return self._ow_7args(*args, **kwds)

    def putwin(self, *args, **kwds):
        return uc.putwin(self.scr, *args, **kwds)

    def redrawln(self, *args, **kwds):
        return uc.wredrawln(self.scr, *args, **kwds)

    def redrawwin(self, *args, **kwds):
        return uc.redrawwin(self.scr, *args, **kwds)

    def refresh(self, *args, **kwds):
        return uc.wrefresh(self.scr, *args, **kwds)

    def scroll(self, *args, **kwds):
        return uc.wscrl(self.scr, *args, **kwds)

    def scrollok(self, *args, **kwds):
        return uc.scrollok(self.scr, *args, **kwds)

    def setscrreg(self, *args, **kwds):
        return uc.wsetscrreg(self.scr, *args, **kwds)

    def standend(self, *args, **kwds):
        return uc.wstandend(self.scr, *args, **kwds)

    def standout(self, *args, **kwds):
        return uc.wstandout(self.scr, *args, **kwds)

    def subpad(self, *args, **kwds):
        return PadObj(uc.subpad(self.scr, *args, **kwds))

    def subwin(self, *args, **kwds):
        return WinObj(uc.subwin(self.scr, *args, **kwds))

    def syncdown(self, *args, **kwds):
        return uc.wsyncdown(self.scr, *args, **kwds)

    def syncok(self, *args, **kwds):
        return uc.syncok(self.scr, *args, **kwds)

    def syncup(self, *args, **kwds):
        return uc.syncup(self.scr, *args, **kwds)

    def timeout(self, *args, **kwds):
        return uc.wtimeout(self.scr, *args, **kwds)

    def touchline(self, *args, **kwds):
        return uc.wtouchline(self.scr, *args, **kwds)

    def touchwin(self, *args, **kwds):
        return uc.touchwin(self.scr, *args, **kwds)

    def vline(self, *args, **kwds):
        return self._overload(args, kwds, 2, uc.wvline, uc.mvwvline)


class PadObj(WinObj):
    """Pad object from curses"""
    def refresh(self, *args, **kwds):
        return uc.prefresh(self.scr, *args, **kwds)


# Wrapper function
def initscr():
    stdscr = uc.initscr()
    return WinObj(stdscr)


def newpad(*args, **kwds):
    return PadObj(uc.newpad(*args, **kwds))


def newwin(*args, **kwds):
    return WinObj(uc.newwin(*args, **kwds))


def wrapper(func, *args, **kwds):
    """Wrapper function from curses."""

    try:
        # Initialize curses
        stdscr = initscr()

        noecho()
        cbreak()

        stdscr.keypad(1)

        try:
            start_color()
        except:
            pass

        return func(stdscr, *args, **kwds)
    finally:
        if 'stdscr' in locals():
            stdscr.keypad(0)
            echo()
            nocbreak()
            endwin()

# --- FUNCTIONS ---
