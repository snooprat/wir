# A simple py curses toolkit

import curses
import curses.panel as cpanel


# Constants
F_TOP = 1
F_MIDDLE = 2
F_BOTTOM = 3
F_LEFT = 4
F_CENTER = 5
F_RIGHT = 6

def _overloadyx(func, y, x, *args):
    """Overload curses y x functions"""
    if y is not None and x is not None:
        func(y, x, *args)
    else:
        func(*args)

def _split_text(text, nrows, ncols):
    """Split text in lines"""
    lines = text.splitlines()
    result = []
    for l in lines:
        current_line = ''
        line_words = l.split(' ')
        for word in line_words:
            if len(current_line + word) > ncols:
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
        if len(line) > ncols:
            result[i] = line[:ncols-3] + '...'
    return result

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
        self.has_border = False

    def addch(self, ch, y=None, x=None, attr=0):
        _overloadyx(self.win.addch, y, x, ch, attr)

    def addstr(self, str, y=None, x=None, attr=0, n=None):
        if n is not None:
            _overloadyx(self.win.addnstr, y, x, str, n, attr)
        else:
            _overloadyx(self.win.addstr, y, x, str, attr)

    def hline(self, ch, n, y=None, x=None):
        _overloadyx(self.win.hline, y, x, ch, n)

    def vline(self, ch, n, y=None, x=None):
        _overloadyx(self.win.vline, y, x, ch, n)

    def insch(self, ch, y=None, x=None, attr=0):
        _overloadyx(self.win.insch, y, x, ch, attr)

    def insstr(self, str, y=None, x=None, attr=0, n=None):
        if n is not None:
            _overloadyx(self.win.insnstr, y, x, str, n, attr)
        else:
            _overloadyx(self.win.insstr, y, x, str, attr)

    def instr(self, str, n, y=None, x=None):
        _overloadyx(self.win.instr, y, x, str, n)

    def insertln(self, nlines=1):
        self.win.insdelln(nlines)

    def deleteln(self, nlines=1):
        self.win.insdelln(-nlines)

    def bkgd(self, ch, attr=0):
        self.win.bkgd(ch, attr)

    def border(self):
        self.win.border()
        self.has_border = True

    def chgat(slef, attr, num=None, y=None, x=None):
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
        self.win.overlay(destwin, sminrow, smincol, dminrow, dmincol,
                    dmaxrow, dmaxcol)

    def overwrite(self, destwin, sminrow=None, smincol=None, dminrow=None,
            dmincol=None, dmaxrow=None, dmaxcol=None):
        self.win.overwrite(destwin, sminrow, smincol, dminrow, dmincol,
                    dmaxrow, dmaxcol)

    def resize(self, nrows, ncols):
        self.win.resize(nrows, ncols)

    def redrawln(self, beg, num):
        self.win.redrawln(beg, num)

    def refresh(self, pminrow=None, pmincol=None, sminrow=None, smincol=None,
            smaxrow=None, smaxcol=None):
        self.win.refresh(pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol)

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

    def newlabel(self, label, h=None, w=None, y=None, x=None, h_align=F_LEFT,
            v_align=F_TOP):
        # Pass object default value
        h = self._h if h is None else h
        w = self._w if w is None else w
        y = self._y if y is None else y
        x = self._x if x is None else x
        # if self.has_border:
        #     h = (self._h-2) if h > (self._h-2) else h
        #     w = (self._w-2) if w > (self._w-2) else w
        #     y = y + 1
        #     x = x + 1
        return Label(self, label, h, w, y, x, h_align, v_align)


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

    def _pad_init(self, nrows, ncols):
        if self.pad is None:
            pad = curses.newpad(nrows, ncols)
            self.pad = Frame(pad)
        return self.pad

    def _pad_update(self, sminrow, smincol):
        self.pad.overwrite(self.win, sminrow, smincol, 0, 0, self._h, self._w)

    def update(self):
        pass


class Label(Widget):
    """A simple Label"""

    def __init__(self, layout, label, h, w, y, x, h_align, v_align):
        # run parent class init function.
        super(Label, self).__init__(layout, h, w, y, x)
        self._text = _split_text(label, h, w)
        self._h_align = h_align
        self._v_align = v_align
        self.update()

    def update(self):
        # The first line position
        y = self._y + self._h//2 - len(self._text)//2 - 1
        for i, l in enumerate(self._text):
            text = l.center(self._w)
            self.addstr(text, y+i, self._x)

    def highlight(self, word, color):
        pass


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
