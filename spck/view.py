import spck
import spck.scurses as curses
import spck.panel as cpanel


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


def _all_none(*args):
    for arg in args:
        if arg is not None:
            return False
    return True


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
        self.callback_keypress = None

    def on_keypress(self, ch):
        _run_if_exist(self.callback_keypress, ch)

    def show(self):
        self.panel.show()

    def hide(self):
        self.panel.hide()

    def newlabel(self, h=None, w=None, y=0, x=0):
        # Pass object default value
        h = self._h if h is None else h
        w = self._w if w is None else w
        return LabelView(self, h, w, y, x)

    def newbox(self, h=None, w=None, y=0, x=0):
        h = self._h if h is None else h
        w = self._w if w is None else w
        box = self.win.derwin(h, w, y, x)
        box.border()

    def newbutton(self, h, w, y=0, x=0):
        return ButtonView(self, h, w, y, x)


class Widget(object):
    """
    A Widget is a re-usable component that can be used to create a simple
    GUI.
    """

    def __init__(self, layout, h, w, y, x):
        self.layout = layout
        self._h = h
        self._w = w
        self._y = y
        self._x = x
        self.pad = self._newpad(h, w)
        self.hl_color = curses.A_BOLD
        self.hl_mark = spck.IGNORE_CH

    def _newpad(self, h, w):
        return curses.newpad(h+1, w)  # +1 to fix last space cannot addstr.

    def addhstr(self, str, y=None, x=None, attr=0):
        text = str.split(self.hl_mark)
        for i, t in enumerate(text):
            if i == 0:
                self.pad.addstr(y, x, t, attr)
            elif i % 2 == 0:
                self.pad.addstr(t, attr)
            elif i % 2 == 1:
                self.pad.addstr(t, self.hl_color)

    def addwstr(self, str, attr=0, v_align=0, h_align=0):
        lines = _align_text(str, self._h, self._w, v_align, h_align,
                            self.hl_mark)
        for i, text in enumerate(lines):
            self.addhstr(text, i, 0, attr)

    def refresh(self, pad=None, win=None):
        pad = self.pad if pad is None else pad
        win = self.layout.win if win is None else win
        y = self._y
        x = self._x
        maxrows = y + self._h - 1
        maxcols = x + self._w - 1
        pad.overwrite(win, 0, 0, y, x, maxrows, maxcols)


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

    def update(self, label=None, attr=None, v_align=None, h_align=None):
        """Update Label status"""
        if not _all_none(label, attr, v_align, h_align):
            self._text = self._text if label is None else label
            self._attr = self._attr if attr is None else attr
            self._v_align = self._v_align if v_align is None else v_align
            self._h_align = self._h_align if h_align is None else h_align
            self.pad.clear()
            self.addwstr(self._text, self._attr, self._v_align, self._h_align)
        self.refresh()

    def _init_focus_pad(self):
        if self._focus_pad is None:
            self._focus_pad = self._newpad(self._h, self._w)
            self.pad.overwrite(self._focus_pad)
            for y in range(self._h):
                self._focus_pad.chgat(y, 0, self.focus_color)

    @property
    def is_focused(self):
        return self._is_focused

    @is_focused.setter
    def is_focused(self, value):
        if value and not self._is_focused:
            self._init_focus_pad()
            self.refresh(self._focus_pad)
        elif not value and self._is_focused:
            self.refresh()
        self._is_focused = value


class ButtonView(LabelView):
    """A simple Button"""

    def __init__(self, layout, h, w, y, x):
        super().__init__(layout, h, w, y, x)
        self.update(h_align=spck.H_CENTER)
        self.btn_l = None
        self.btn_r = None
        self.btn_u = None
        self.btn_d = None
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

    def _next_btn(self, btn):
        if btn:
            self.is_selected = False
            self.btn.is_selected = True

    def go_left(self):
        self._next_btn(self.btn_l)

    def go_right(self):
        self._next_btn(self.btn_r)

    def go_up(self):
        self._next_btn(self.btn_u)

    def go_down(self):
        self._next_btn(self.btn_d)


class ListView(Widget):
    """A simple List"""

    def __init__(self, layout, h, w, y, x):
        super().__init__(layout, h, w, y, x)
        self.head = None
        self.current = None
        self.len = 0

    def additem(self, data):
        if self.len < self._h:
            newitem = ButtonView(self.layout, 1, self._w, self.len, 0)
            if self.head is None:
                self.head = newitem
            else:
                item = self.head
                while item.btn_d is not None:
                    item = item.btn_d
                item.btn_d = newitem
                newitem.btn_u = item

    def clearitem(self):
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


class TabView(Widget):
    pass
