import curses
import curses.panel as cpanel

import spck


def _split_text(text, nrows, ncols, ignore=spck.IGNORE_CH):
    """Split text in lines"""
    lines = text.splitlines()
    result = []
    for l in lines:
        current_line = ''
        line_words = l.split(' ')
        for word in line_words:
            cl_len = len(current_line.replace(ignore, '')
                         + word.replace(ignore, ''))
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


def _align_text(text, nrows, ncols, v_align, h_align, ignore=spck.IGNORE_CH):
    """Align text"""
    lines = _split_text(text, nrows, ncols, ignore)
    lines_num = len(lines)
    result = []
    # Vertical align
    if v_align is spck.V_MIDDLE:
        lines_add = (nrows-lines_num) // 2
    elif v_align is spck.V_BOTTOM:
        lines_add = (nrows-lines_num)
    else:
        lines_add = 0
    v_aligned_lines = [''] * lines_add
    v_aligned_lines.extend(lines)
    # Horizontal align
    if h_align is spck.H_CENTER:
        for l in v_aligned_lines:
            result.append(l.center(ncols+l.count(ignore)))
    elif h_align is spck.H_RIGHT:
        for l in v_aligned_lines:
            result.append(l.rjust(ncols+l.count(ignore)))
    else:
        result = v_aligned_lines

    return result


def _run_if_exist(func, *args, **kwds):
    if func is not None:
        func(*args, **kwds)


class Layout(object):
    """A Layout is a display area."""

    def __init__(self, h, w, y=0, x=0):
        self._h = h
        self._w = w
        self._y = y
        self._x = x
        self.win = curses.newwin(h, w, y, x)
        self.pad = curses.newpad(h, w)
        self.panel = cpanel.new_panel(self.win)
        self.panel.set_userptr(self)
        self._need_refresh = False
        self.callback_keypress = None

    def on_keypress(self, ch):
        _run_if_exist(self.callback_keypress, ch)

    def show(self):
        self.refresh()
        self.panel.show()

    def hide(self):
        self.panel.hide()

    def refresh(self):
        if self._need_refresh:
            self.pad.overwrite(self.win, 0, 0, 0, 0, self._h-1, self._w-1)
            self._need_refresh = False

    def newlabel(self, h=None, w=None, y=0, x=0):
        # Pass object default value
        h = self._h if h is None else h
        w = self._w if w is None else w
        return LabelView(self, h, w, y, x)


class Widget(object):
    """A Widget is a re-usable component that can be used to create a simple GUI.
    """

    def __init__(self, layout, h, w, y, x):
        self.layout = layout
        self._h = h
        self._w = w
        self._y = y
        self._x = x
        self.win = layout.pad.derwin(h, w, y, x)
        self.hl_color = curses.A_BOLD
        self.hl_mark = spck.IGNORE_CH

    def addhstr(self, str, y=None, x=None, attr=0):
        text = str.split(self.hl_mark)
        for i, t in enumerate(text):
            if i == 0:
                self.win.addstr(y, x, t, attr)
            elif i % 2 == 0:
                self.win.addstr(t, attr)
            elif i % 2 == 1:
                self.win.addstr(t, self.hl_color)

    def addwstr(self, str, attr=0, v_align=0, h_align=0):
        lines = _align_text(str, self._h, self._w, v_align, h_align,
                            self.hl_mark)
        for i, text in enumerate(lines):
            self.addhstr(text, i, 0, attr)

    def refresh(self):
        self.layout._need_refresh = True

    def clear(self):
        self.win.clear()


class LabelView(Widget):
    """A simple Label"""

    def __init__(self, layout, h, w, y, x):
        # run parent class init function.
        super().__init__(layout, h, w, y, x)
        self._text = ''
        self._h_align = 0
        self._v_align = 0
        self._attr = 0
        self._is_focused = False
        self.focus_color = curses.A_REVERSE
        self._focus_pad = None
        self._origin_pad = None

    def update(self, label=None, attr=None, v_align=None, h_align=None):
        """Update Label status"""
        label = self._text if label is None else label
        attr = self._attr if attr is None else attr
        v_align = self._v_align if v_align is None else v_align
        h_align = self._h_align if h_align is None else h_align
        self.win.clear()
        self.addwstr(label, attr, v_align, h_align)
        self.refresh()

    def _init_origin_pad(self):
        if self._origin_pad is None:
            self._origin_pad = curses.newpad(self._h, self._w)
            maxrow = self._h - 1
            maxcol = self._w - 1
            self.win.overwrite(self._origin_pad, 0, 0, 0, 0, maxrow, maxcol)

    def _init_focus_pad(self):
        if self._focus_pad is None:
            self._focus_pad = curses.newpad(self._h, self._w)
            maxrow = self._h - 1
            maxcol = self._w - 1
            self.win.overwrite(self._focus_pad, 0, 0, 0, 0, maxrow, maxcol)
            for y in range(self._h):
                self._focus_pad.chgat(y, 0, self.focus_color)

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
            self._init_origin_pad()
            self._init_focus_pad()
            if self._focus_pad is not None:
                self.win.clear()
                self._focus_pad.overwrite(self.win, 0, 0, 0, 0, maxrow, maxcol)
            self.refresh()
        elif not value and self._is_focused:
            if self._origin_pad is not None:
                self.win.clear()
                self._origin_pad.overlay(self.win, 0, 0, 0, 0, maxrow, maxcol)
            self.refresh()
        self._is_focused = value


class ButtonView(LabelView):
    """A simple Button"""

    def __init__(self, layout, h, w, y, x):
        super().__init__(layout, h, w, y, x)
        self.pre_btn = None
        self.next_btn = None
        self._is_selected = False
        self.callback_select = None
        self.callback_enter = None

    @property
    def is_selected(self):
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value):
        if value:
            self.is_focused = True
            _run_if_exist(self.callback_select)
        else:
            self.is_focused = False

    def on_enter(self):
        _run_if_exist(self.callback_enter)


class ListView(Widget):
    """A simple List"""

    def __init__(self, layout, h, w, y, x):
        super().__init__(layout, h, w, y, x)
        self.current_item = None

    def additem(self, data):
        pass

    def clearitem(self):
        pass

    def scrollbar(self):
        pass


class MapView(Widget):
    """A simple Map"""

    def __init__(self, layout, h, w, y, x, maph, mapw):
        super().__init__(layout, h, w, y, x)
        self._maph = maph
        self._mapw = mapw
        self._mapdrawy = 0
        self._mapdrawx = 0
        self._cur_y = 0
        self._cur_x = 0

    def draw_map(self):
        pass

    def move_map(self):
        pass
