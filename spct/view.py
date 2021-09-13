import curses
import curses.panel as cpanel

import spct.constant as CONST
from spct.event import KeyEvent


def _split_text(text, nrows, ncols, strong=CONST.CH_HIGHLIGHT):
    """Split text in lines"""
    lines = text.splitlines()
    result = []
    for line in lines:
        current_line = ''
        line_words = line.split(' ')
        for word in line_words:
            cl_len = len(current_line.replace(strong, '')
                         + word.replace(strong, ''))
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
        if len(line.replace(strong, '')) > ncols:
            result[i] = line[:ncols-3] + '...'
    return result


def _align_text(text, nrows, ncols, v_align, h_align,
                ignore=CONST.CH_HIGHLIGHT):
    """Align text"""
    lines = _split_text(text, nrows, ncols, ignore)
    lines_num = len(lines)
    result = []
    # Vertical align
    if v_align is CONST.AL_MIDDLE:
        lines_add = (nrows-lines_num) // 2
    elif v_align is CONST.AL_BOTTOM:
        lines_add = (nrows-lines_num)
    else:
        lines_add = 0
    v_aligned_lines = [''] * lines_add
    v_aligned_lines.extend(lines)
    # Horizontal align
    if h_align is CONST.AL_CENTER:
        for line in v_aligned_lines:
            result.append(line.center(ncols+line.count(ignore)))
    elif h_align is CONST.AL_RIGHT:
        for line in v_aligned_lines:
            result.append(line.rjust(ncols+line.count(ignore)))
    else:
        result = v_aligned_lines

    return result


class ViewLayout(object):
    """A view layout is a display area to display widget."""

    def __init__(self, h, w, y=0, x=0, colors=None):
        self._h = h
        self._w = w
        self._y = y
        self._x = x
        self._win = curses.newwin(h, w, y, x)
        self.win.keypad(True)
        self._panel = cpanel.new_panel(self.win)
        self.panel.set_userptr(self)
        self.viewctr = None
        self._colors = colors
        self.init_view()

    @property
    def height(self):
        return self._h

    @property
    def width(self):
        return self._w

    @property
    def win(self):
        return self._win

    @property
    def panel(self):
        return self._panel

    def init_view(self):
        """Overload view initial code"""
        pass

    def set_ctr(self, ctr):
        self.viewctr = ctr

    def run_ctr(self):
        ch = KeyEvent(self.win.getch())
        self.viewctr.on_event(ch)

    def get_color(self, color):
        return self._colors.get_color(color)

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
        return BoxView(self, h, w, y, x)

    def newbutton(self, h, w, y=0, x=0, text="Button", bid='b0'):
        return ButtonView(self, h, w, y, x, text, bid)

    def newmap(self, map_data, h, w, y=0, x=0):
        return MapView(self, map_data, h, w, y, x)


class Widget(object):
    """
    A Widget is a re-usable component that can be used to create a simple GUI.
    """

    def __init__(self, layout, h, w, y, x, pad_h=None, pad_w=None):
        self._layout = layout
        self._h = h
        self._w = w
        self._y = y
        self._x = x
        self._pad_draw_y = 0
        self._pad_draw_x = 0
        self._padh = h if pad_h is None else pad_h
        self._padw = w if pad_w is None else pad_w
        self._pad = self._newpad(self._padh, self._padw)
        # calculate draw area
        diff_y = 0
        diff_x = 0
        maxh = self._h
        maxw = self._w
        if self._padh < self._h:
            diff_y = int((self._h - self._padh) / 2)
            maxh = self._padh
        if self._padw < self._w:
            diff_x = int((self._w - self._padw) / 2)
            maxw = self._padw
        self._draw_from_y = self._y + diff_y
        self._draw_from_x = self._x + diff_x
        self._draw_to_y = self._draw_from_y + maxh - 1
        self._draw_to_x = self._draw_from_x + maxw - 1
        self._draw_maxh = maxh
        self._draw_maxw = maxw
        # functions and colors
        self.addstr = self.pad.addstr
        self.addch = self.pad.addch
        self.hl_color = CONST.A_BOLD
        self.hl_mark = CONST.CH_HIGHLIGHT

    @property
    def pad(self):
        return self._pad

    @property
    def layout(self):
        return self._layout

    @property
    def pad_draw_y(self):
        return self._pad_draw_y

    @pad_draw_y.setter
    def pad_draw_y(self, value):
        # check the value is correct
        if value <= 0:
            value = 0
        elif value > (maxy := self._padh - self._h):
            value = maxy if maxy > 0 else 0
        self._pad_draw_y = value

    @property
    def pad_draw_x(self):
        return self._pad_draw_x

    @pad_draw_x.setter
    def pad_draw_x(self, value):
        # check the value is correct
        if value <= 0:
            value = 0
        elif value > (max_x := self._padw - self._w):
            value = max_x if max_x > 0 else 0
        self._pad_draw_x = value

    def _newpad(self, h, w):
        # Pad height +1 to fix last space cannot addstr.
        return curses.newpad(h+1, w)

    def addhstr(self, str, y=None, x=None, attr=0):
        """Add highlight text"""
        text = str.split(self.hl_mark)
        for i, t in enumerate(text):
            if i == 0:
                self.addstr(y, x, t, attr)
            elif i % 2 == 0:
                self.addstr(t, attr)
            elif i % 2 == 1:
                self.addstr(t, self.hl_color)

    def addwstr(self, str, attr=0, v_align=0, h_align=0):
        """Add align and hightlight text"""
        lines = _align_text(str, self._h, self._w, v_align, h_align,
                            self.hl_mark)
        for i, text in enumerate(lines):
            self.addhstr(text, i, 0, attr)

    def update(self, pad=None, win=None, pad_y=None, pad_x=None):
        """Overwrite Widget pad text to Layout window area."""
        pad = self.pad if pad is None else pad
        win = self.layout.win if win is None else win
        if pad_y is not None:
            self.pad_draw_y = pad_y
        if pad_x is not None:
            self.pad_draw_x = pad_x
        pad.overwrite(win, self.pad_draw_y, self.pad_draw_x,
                      self._draw_from_y, self._draw_from_x,
                      self._draw_to_y, self._draw_to_x)


class LabelView(Widget):
    """A simple Label"""

    def __init__(self, layout, h, w, y, x):
        # run parent class init function.
        super().__init__(layout, h, w, y, x)
        self._text = 'Lable'
        self._h_align = 0
        self._v_align = 0
        self._attr = 0

    def set_text(self, label=None, attr=None, v_align=None, h_align=None):
        """Set Label text"""
        self._text = self._text if label is None else label
        self._attr = self._attr if attr is None else attr
        self._v_align = self._v_align if v_align is None else v_align
        self._h_align = self._h_align if h_align is None else h_align
        self.pad.clear()
        self.addwstr(self._text, self._attr, self._v_align, self._h_align)
        self.update()


class BoxView(object):

    """A simple Box Border and Tile"""

    def __init__(self, layout, h, w, y, x):
        """TODO: to be defined.

        :h: TODO
        :w: TODO
        :y: TODO
        :x: TODO

        """
        self._layout = layout
        self._h = h
        self._w = w
        self._y = y
        self._x = x
        self._box = self._layout.win.derwin(h, w, y, x)
        self._box.border()

    def set_title(self, text='TITLE', attr=CONST.A_BOLD):
        # Add title
        title_len = len(text) + 2
        self._title = self._layout.newlabel(1, title_len, 0,
                                            int((self._w-title_len)/2))
        self._title.set_text(text, attr, h_align=CONST.AL_CENTER)


class ButtonView(LabelView):
    """A simple Button"""

    def __init__(self, layout, h, w, y, x, text, bid):
        super().__init__(layout, h, w, y, x)
        self._focus = False
        self._focus_pad = self._newpad(self._h, self._w)
        self.set_text(text, h_align=CONST.AL_CENTER)
        self._bid = bid

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, value):
        if self._focus != value:
            self._focus = value
            self.update_focus()

    def update_focus(self):
        if self._focus:
            self.update(self._focus_pad)
        else:
            self.update()

    def set_text(self, label=None, attr=None, v_align=None, h_align=None):
        super().set_text(label, attr, v_align, h_align)
        self.pad.overwrite(self._focus_pad)
        self._focus_pad.bkgd(CONST.A_REVERSE)
        self.update_focus()

    def get_text(self):
        return self._text

    def get_id(self):
        return self._bid


class ListView(Widget):
    """A simple List"""

    def __init__(self, layout, h, w, y, x):
        super().__init__(layout, h, w, y, x)
        self.head = None
        self.current = None
        self.len = 0

    # def add_item(self, data):
    #     if self.len < self._h:
    #         newitem = ButtonView(self.layout, 1, self._w, self.len, 0)
    #         if self.head is None:
    #             self.head = newitem
    #         else:
    #             item = self.head
    #             while item.btn_d is not None:
    #                 item = item.btn_d
    #             item.btn_d = newitem
    #             newitem.btn_u = item

    def clear_item(self):
        pass


class MapView(Widget):
    """A simple Map"""

    def __init__(self, layout, map_data, h, w, y, x):
        self._map = map_data
        _maph = self._map[CONST.CH_MAP_MAPH]
        _mapw = self._map[CONST.CH_MAP_MAPW]
        super().__init__(layout, h, w, y, x, _maph, _mapw)
        self._cur_gy = 0
        self._cur_gx = 0
        self._grid = []
        self._grid_len = 3
        self._gridh = 0
        self._gridw = 0
        self._layers = []
        self.map_layer = None
        self.init_map()
        self.init_grid()

    @property
    def mapdrawy(self):
        return self.pad_draw_y

    @mapdrawy.setter
    def mapdrawy(self, value):
        self.pad_draw_y = value

    @property
    def mapdrawx(self):
        return self.pad_draw_x

    @mapdrawx.setter
    def mapdrawx(self, value):
        self.pad_draw_x = value

    @property
    def cur_gy(self):
        return self._cur_gy

    @cur_gy.setter
    def cur_gy(self, value):
        if value < 0:
            value = 0
        elif value > (max_gy := self._gridh - 1):
            value = max_gy
        self._cur_gy = value

    @property
    def cur_gx(self):
        return self._cur_gx

    @cur_gx.setter
    def cur_gx(self, value):
        if value < 0:
            value = 0
        elif value > (max_gx := self._gridw - 1):
            value = max_gx
        self._cur_gx = value

    def init_map(self):
        mapdata = self._map[CONST.CH_MAP_MAP].replace(' ', '')
        self._margin = self._map[CONST.CH_MAP_MARGIN]
        cell = self._map[CONST.CH_MAP_CELL]
        self.map_layer = self.add_layer()  # create a base map
        for t in mapdata:
            color_name = cell[t].get(CONST.CH_MAP_COLOR)
            color = self.layout.get_color(color_name)
            map_char = cell[t][CONST.CH_MAP_CHAR]
            self.map_layer.addch(map_char, color)
        self.update()

    def init_grid(self):
        grid_h = self._map[CONST.CH_MAP_GRIDH]
        grid_w = self._map[CONST.CH_MAP_GRIDW]
        grid_len = self._map.get(CONST.CH_MAP_GRID_LEN,
                                 CONST.DEF_MAP_GRID_LEN)
        grid_offset = self._map.get(CONST.CH_MAP_GRID_OFFSET,
                                    CONST.DEF_MAP_GRID_OFFSET)
        grid_space = self._map.get(CONST.CH_MAP_GRID_SPACE,
                                   CONST.DEF_MAP_GRID_SPACE)
        grid_starty = self._map.get(CONST.CH_MAP_GRIDY, CONST.DEF_MAP_GRIDY)
        grid_startx = self._map.get(CONST.CH_MAP_GRIDX, CONST.DEF_MAP_GRIDX)
        self._gridh = grid_h
        self._gridw = grid_w
        self._grid_len = grid_len
        self._grid_space = grid_space
        self._margin_y = self._margin
        self._margin_x = self._margin * (self._grid_len+self._grid_space)
        for row in range(grid_h):
            self._grid.append([])  # create a row
            for col in range(grid_w):
                grid_y = row + grid_starty
                offset = grid_offset * int(row % 2)
                grid_x = col * (grid_len+grid_space) + offset + grid_startx
                self._grid[row].append([grid_y, grid_x])

    def add_layer(self):
        layer = MapLayer(self._newpad(self._padh, self._padw))
        self._layers.append(layer)
        return layer

    def update(self, pad=None, win=None, pad_y=None, pad_x=None,
               all_layers=False):
        if all_layers:
            for layer in self._layers:
                if layer.is_visible:
                    layer.pad.overlay(self.pad)
        super().update(pad, win, pad_y, pad_x)

    def move_map(self, new_y, new_x):
        self.mapdrawy = new_y
        self.mapdrawx = new_x

    def move_cusor(self, gy, gx):
        pre_cur_gy = self.cur_gy
        pre_cur_gx = self.cur_gx
        self.cur_gy = gy
        self.cur_gx = gx
        # Highlight cursor hex
        self.highlight_hex(pre_cur_gy, pre_cur_gx, False)
        self.highlight_hex(self.cur_gy, self._cur_gx, True)
        # Move the map when the cursor move to the edge margin
        is_redraw = False
        cur_y, cur_x = self.get_grid_yx(self.cur_gy, self.cur_gx)
        draw_y = self.pad_draw_y
        draw_x = self.pad_draw_x
        move_y = draw_y
        move_x = draw_x
        if draw_y > 0 and draw_y > (new := cur_y - self._margin_y):
            move_y = new
            is_redraw = True
        if ((old := draw_y + self._draw_maxh) < self._padh and
                old < (new := cur_y + 1 + self._margin_y)):
            move_y = new - self._draw_maxh
            is_redraw = True
        if draw_x > 0 and draw_x > (new := cur_x - self._margin_x):
            move_x = new
            is_redraw = True
        if ((old := draw_x + self._draw_maxw) < self._padw and
                old < (new := cur_x + self._grid_len + self._margin_x)):
            move_x = new - self._draw_maxw
            is_redraw = True
        if is_redraw:
            self.move_map(move_y, move_x)

    def get_grid_yx(self, gy, gx):
        return self._grid[gy][gx]

    def get_hex(self, gy, gx):
        result = []
        hex_y, hex_x = self.get_grid_yx(gy, gx)
        for i in range(self._grid_len):
            result.append([self.pad.inch(hex_y, hex_x+i), hex_y, hex_x+i])
        return result

    def set_hex(self, hex_data, hex_attr):
        pass

    def highlight_hex(self, gy, gx, is_on):
        hex_data = self.get_hex(gy, gx)
        for h in hex_data:
            hex_d, hex_y, hex_x = h
            self.pad.move(hex_y, hex_x)
            if is_on:
                self.pad.addch(hex_d | CONST.A_REVERSE)
            else:
                self.pad.addch(hex_d & ~CONST.A_REVERSE)


class MapLayer(object):
    """ Map layer to display object on map."""

    def __init__(self, pad):
        self._pad = pad
        self._is_visible = True
        self.addch = self._pad.addch
        self.addstr = self._pad.addstr

    @property
    def pad(self):
        return self._pad

    @property
    def is_visible(self):
        return self._is_visible

    def show(self):
        self._is_visible = True

    def hide(self):
        self._is_visible = False


class TabView(Widget):
    pass
