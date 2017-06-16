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
        ch = top_layout.win.getch()
        top_layout.keyfunc(ch)


class Layout(object):
    """A Layout is a display area."""

    def __init__(self, h, w, y=0, x=0):
        self._h = h
        self._w = w
        self._y = y
        self._x = x
        self.win = curses.newwin(h, w, y, x)
        self.panel = cpanel.new_panel(self.win)
        self.panel.set_userptr(self)
        self.keyfunc = None

    def set_keyfunc(self, func):
        self.keyfunc = func

    def show(self):
        self.panel.show()

    def hide(self):
        self.panel.hide()

    def newlabel(self, h=None, w=None, y=0, x=0):
        # Pass object default value
        h = self._h if h is None else h
        w = self._w if w is None else w
        return Label(self, h, w, y, x)


class Widget(object):
    """A Widget is a re-usable component that can be used to create a simple GUI.
    """

    def __init__(self, layout, h, w, y, x):
        self.layout = layout
        self._h = h
        self._w = w
        self._y = y
        self._x = x
        self.win = layout.win.derwin(h, w, y, x)
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
                self.win.addstr(y, x, t, attr)
            elif i%2 == 0:
                self.win.addstr(t, attr)
            elif i%2 == 1:
                self.win.addstr(t, self.hl_color)

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
        self.focused_pad = None
        self.origin_pad = None

    def update(self, label=None, attr=None, v_align=None, h_align=None):
        """Update Label status"""
        label = self._text if label is None else label
        attr = self._attr if attr is None else attr
        v_align = self._v_align if v_align is None else v_align
        h_align = self._h_align if h_align is None else h_align
        self.win.clear()
        self.addwstr(label, attr, v_align, h_align)

    @property
    def is_focused(self):
        return self._is_focused

    @is_focused.setter
    def is_focused(self, value):
        h = self._h
        w = self._w
        maxrow = h - 1
        maxcol = w - 1
        if value and not self._is_focused:
            if self.origin_pad is None:
                self.origin_pad = curses.newpad(h, w)
                self.win.overwrite(self.origin_pad, 0, 0, 0, 0, maxrow, maxcol)
            if self.focused_pad is None:
                self.focused_pad = curses.newpad(h, w)
                self.win.overwrite(self.focused_pad, 0, 0, 0, 0, maxrow, maxcol)
                for y in range(h):
                    self.focused_pad.chgat(y, 0, self.focused_color)
            if self.focused_pad is not None:
                self.win.clear()
                self.focused_pad.overwrite(self.win, 0, 0, 0, 0, maxrow, maxcol)
            self.win.refresh()
        elif not value and self._is_focused:
            if self.origin_pad is not None:
                self.win.clear()
                self.origin_pad.overlay(self.win, 0, 0, 0, 0, maxrow, maxcol)
            self.win.refresh()
        self._is_focused = value


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
