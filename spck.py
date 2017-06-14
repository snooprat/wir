# A simple py curses toolkit

import curses
import curses.panel as cpanel


# Constants
V_TOP = 1
V_MIDDLE = 2
V_BOTTOM = 3
H_LEFT = 4
H_CENTER = 5
H_RIGHT = 6

IGNORE_CH = '`'

def _is_none(*args):
    for arg in args:
        if arg is not None:
            return False
    return True

def _overloadyx(func, y, x, *args):
    """Overload curses y x functions"""
    if _is_none(y, x):
        func(*args)
    else:
        func(y, x, *args)

def _overload(func, *args):
    if _is_none(*args):
        func()
    else:
        func(*arg)

def _overloadfix(func, fix_arg, *args):
    if _is_none(*args):
        func(fix_arg)
    else:
        func(fix_arg, *args)

def _split_text(text, nrows, ncols, ignore=IGNORE_CH):
    """Split text in lines"""
    lines = text.splitlines()
    result = []
    for l in lines:
        current_line = ''
        line_words = l.split(' ')
        for word in line_words:
            cl_len = len(current_line.replace(ignore, '')+word.replace(ignore, ''))
            if current_line and cl_len > ncols:
                result.append(current_line.rstrip())
                current_line = word + ' '
            else:
                current_line += word + ' '
        result.append(current_line.rstrip())
    # Check for height.
    if len(result) > nrows:
        result = result[:nrows]
        result[nrows-1] = result[nrows-1][:ncols-3] + '...'
    # Check for width.
    for i, line in enumerate(result):
        if len(line.replace(ignore, '')) > ncols:
            result[i] = line[:ncols-3] + '...'
    return result

def _align_text(text, nrows, ncols, v_align, h_align, ignore=IGNORE_CH):
    """Align text"""
    lines = _split_text(text, nrows, ncols, ignore)
    lines_num = len(lines)
    result = []
    # Vertical align
    if v_align is V_MIDDLE:
        lines_add = (nrows-lines_num) // 2
    elif v_align is V_BOTTOM:
        lines_add = (nrows-lines_num)
    else:
        lines_add = 0
    v_aligned_lines = [''] * lines_add
    v_aligned_lines.extend(lines)
    # Horizontal align
    if h_align is H_CENTER:
        for l in v_aligned_lines:
            result.append(l.center(ncols+l.count(ignore)))
    elif h_align is H_RIGHT:
        for l in v_aligned_lines:
            result.append(l.rjust(ncols+l.count(ignore)))
    else:
        result = v_aligned_lines

    return result

def add_color(color_number, fg, bg, attr=curses.A_NORMAL):
    curses.init_pair(color_number, fg, bg)
    return curses.color_pair(color_number) | attr

def update():
    """Update screen display"""
    cpanel.update_panels()
    curses.doupdate()

def run():
    """Run the top layout's function."""
    while True:
        top_layout = curses.panel.top_panel().userptr()
        ch = top_layout.getch()
        top_layout.keyfunc(ch)


class Frame(object):
    """Basic window frame based on curses window object."""

    def __init__(self, win):
        self.win = win

    def addch(self, ch, y=None, x=None, attr=0):
        _overloadyx(self.win.addch, y, x, ch, attr)

    def addstr(self, str, y=None, x=None, attr=0):
        _overloadyx(self.win.addstr, y, x, str, attr)

    def hline(self, ch, n, y=None, x=None):
        _overloadyx(self.win.hline, y, x, ch, n)

    def vline(self, ch, n, y=None, x=None):
        _overloadyx(self.win.vline, y, x, ch, n)

    def insch(self, ch, y=None, x=None, attr=0):
        _overloadyx(self.win.insch, y, x, ch, attr)

    def insstr(self, str, y=None, x=None, attr=0):
        _overloadyx(self.win.insstr, y, x, str, attr)

    def instr(self, str, n, y=None, x=None):
        _overloadyx(self.win.instr, y, x, str, n)

    def insertln(self, nlines=1):
        self.win.insdelln(nlines)

    def deleteln(self, nlines=1):
        self.win.insdelln(-nlines)

    def inch(self, y=None, x=None):
        _overloadyx(self.win.inch, y, x)

    def bkgd(self, ch, attr=0):
        self.win.bkgd(ch, attr)

    def border(self):
        self.win.border()

    def chgat(self, attr, y=None, x=None, num=None):
        if num is not None:
            _overloadyx(self.win.chgat, y, x, num, attr)
        else:
            _overloadyx(self.win.chgat, y, x, attr)

    def clear(self):
        self.win.clear()

    def clrtobot(self):
        self.win.clrtobot()

    def clrtoeol(self):
        self.win.clrtoeol()

    def delch(self, y=None, x=None):
        _overloadyx(self.win.delch, y, x)

    def getbegyx(self):
        return self.win.getbegyx()

    def getmaxyx(self):
        return self.win.getmaxyx()

    def getparyx(self):
        return self.win.getparyx()

    def mvwin(self, new_y, new_x):
        self.win.mvwin(new_y, new_x)

    def mvderwin(self, y, x):
        self.win.mvderwin(y, x)

    def getch(self):
        return self.win.getch()

    def getyx(self):
        return self.win.getyx()

    def move(self, new_y, new_x):
        self.win.move(new_y, new_x)

    def overlay(self, destwin, sminrow=None, smincol=None, dminrow=None,
            dmincol=None, dmaxrow=None, dmaxcol=None):
        _overloadfix(self.win.overlay, destwin, sminrow, smincol, dminrow,
                dmincol, dmaxrow, dmaxcol)

    def overwrite(self, destwin, sminrow=None, smincol=None, dminrow=None,
            dmincol=None, dmaxrow=None, dmaxcol=None):
        _overloadfix(self.win.overwrite, destwin, sminrow, smincol, dminrow,
                dmincol, dmaxrow, dmaxcol)

    def resize(self, nrows, ncols):
        self.win.resize(nrows, ncols)

    def redrawln(self, beg, num):
        self.win.redrawln(beg, num)

    def refresh(self, pminrow=None, pmincol=None, sminrow=None, smincol=None,
            smaxrow=None, smaxcol=None):
        _overload(self.win.refresh, pminrow, pmincol, sminrow, smincol,
                smaxrow, smaxcol)

    def derwin(self, nrows, ncols, begin_y, begin_x):
        return self.win.derwin(nrows, ncols, begin_y, begin_x)


class Layout(Frame):
    """A Layout is a display area."""

    def __init__(self, h, w, y=0, x=0):
        self._h = h
        self._w = w
        self._y = y
        self._x = x
        win = curses.newwin(h, w, y, x)
        super(Layout, self).__init__(win)
        self.panel = cpanel.new_panel(self.win)
        self.panel.set_userptr(self)
        self.keyfunc = None

    def set_keyfunc(self, func):
        self.keyfunc = func

    def show(self):
        self.panel.show()

    def hide(self):
        self.panel.hide()

    def newlabel(self, h=None, w=None, y=None, x=None):
        # Pass object default value
        h = self._h if h is None else h
        w = self._w if w is None else w
        y = self._y if y is None else y
        x = self._x if x is None else x
        return Label(self, h, w, y, x)


class Widget(Frame):
    """A Widget is a re-usable component that can be used to create a simple GUI.
    """

    def __init__(self, layout, h, w, y, x):
        self.layout = layout
        self._h = h
        self._w = w
        self._y = y
        self._x = x
        win = layout.derwin(h, w, y, x)
        super(Widget, self).__init__(win)
        self.pad = None
        self.hl_color = curses.A_BOLD
        self.hl_mark = IGNORE_CH

    def _pad_init(self, nrows, ncols):
        if self.pad is None:
            pad = curses.newpad(nrows, ncols)
            self.pad = Frame(pad)
        return self.pad

    def _pad_update(self, sminrow, smincol):
        self.pad.overwrite(self.win, sminrow, smincol, 0, 0, self._h, self._w)

    def addhstr(self, str, y=None, x=None, attr=0):
        text = str.split(self.hl_mark)
        for i, t in enumerate(text):
            if i == 0:
                self.addstr(t, y, x, attr)
            elif i%2 == 0:
                self.addstr(t, attr=attr)
            elif i%2 == 1:
                self.addstr(t, attr=self.hl_color)

    def addwstr(self, str, attr=0, v_align=0, h_align=0):
        lines = _align_text(str, self._h, self._w, v_align, h_align, self.hl_mark)
        for i, text in enumerate(lines):
            self.addhstr(text, i, 0, attr)


class Label(Widget):
    """A simple Label"""

    def __init__(self, layout, h, w, y, x):
        # run parent class init function.
        super(Label, self).__init__(layout, h, w, y, x)
        self._text = ''
        self._h_align = 0
        self._v_align = 0
        self._attr = 0
        self._is_focused = False
        self.focused_color = curses.A_REVERSE
        self.origin_color = []

    def update(self, label=None, attr=None, v_align=None, h_align=None):
        """Update Label status"""
        label = self._text if label is None else label
        attr = self._attr if attr is None else attr
        v_align = self._v_align if v_align is None else v_align
        h_align = self._h_align if h_align is None else h_align
        #self.clear()
        self.addwstr(label, attr, v_align, h_align)

    def _init_origin_color(self):
        if len(self.origin_color) == 0:
            for x in range(self._w):
                self.origin_color.append(self.inch(0,x))

    def _clear_origin_color(self):
        if len(self.origin_color) > 0:
            self.origin_color.clear()

    @property
    def is_focused(self):
        return self._is_focused

    @is_focused.setter
    def is_focused(self, value):
        if value and not self._is_focused:
            self._init_origin_color()
            self.chgat(self.focused_color, 0, 0)
        elif not value and self._is_focused:
            for x in range(self._w):
                for y in range(self._h):
                    i = y * self._w + x
                    ch = chr(self.origin_color[i] & curses.A_CHARTEXT)
                    attr = self.origin_color[i] & curses.A_ATTRIBUTES
                    self.addch(ch, y, x, attr)


class Map(Widget):
    """A simple Map"""

    def __init__(self, layout, h, w, y, x, maph, mapw):
        super(Map, self).__init__(layout, h, w, y, x)
        self._maph = maph
        self._mapw = mapw
        self._pad_init(maph, mapw)
        self._mapdrawy = 0
        self._mapdrawx = 0
        self._cur_y = 0
        self._cur_x = 0

    def draw_map(self):
        self._pad_update(self._mapdrawy, self._mapdrawx)

    def move_map(self):
        pass


class List(Widget):
    pass
