import curses
import curses.panel as cpanel

import spct.constant as const
from spct.event import KeyEvent
from spct.color import ColorMap, chattr


def _split_text(text: str, nrows: int, ncols: int,
                strong: str = const.C_HIGHLIGHT) -> list[str]:
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


def _align_text(text: str, nrows: int, ncols: int, v_align: int, h_align: int,
                ignore: str = const.C_HIGHLIGHT) -> list[str]:
    """Align text"""
    lines = _split_text(text, nrows, ncols, ignore)
    lines_num = len(lines)
    result = []
    # Vertical align
    if v_align is const.A_MIDDLE:
        lines_add = (nrows-lines_num) // 2
    elif v_align is const.A_BOTTOM:
        lines_add = (nrows-lines_num)
    else:
        lines_add = 0
    v_aligned_lines = [''] * lines_add
    v_aligned_lines.extend(lines)
    # Horizontal align
    if h_align is const.A_CENTER:
        for line in v_aligned_lines:
            result.append(line.center(ncols+line.count(ignore)))
    elif h_align is const.A_RIGHT:
        for line in v_aligned_lines:
            result.append(line.rjust(ncols+line.count(ignore)))
    else:
        result = v_aligned_lines

    return result


class ViewLayout(object):
    """A view layout is a display area to display widget."""

    def __init__(self, h: int, w: int, y: int = 0, x: int = 0,
                 colors: ColorMap = None):
        self._h = h
        self._w = w
        self._y = y
        self._x = x
        self._win = curses.newwin(h, w, y, x)
        self.win.keypad(True)
        self._panel = cpanel.new_panel(self.win)
        self.panel.set_userptr(self)
        self._viewctr = None
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

    @property
    def viewctr(self):
        return self._viewctr

    def init_view(self):
        """Overload view initial code"""

    def set_ctr(self, ctr):
        self._viewctr = ctr

    def run_ctr(self):
        ch = KeyEvent(self.win.getch())
        if self.viewctr:
            self.viewctr.on_event(ch)

    def get_color(self, color: const.T_COLOR) -> int:
        result = const.S_COLOR_ERROR
        if isinstance(color, int):
            result = color
        elif self._colors:
            result = self._colors.get_color(color)
        return result

    def show(self):
        self.panel.show()

    def hide(self):
        self.panel.hide()

    def newlabel(self, h: int = None, w: int = None, y: int = 0,
                 x: int = 0) -> 'LabelView':
        # Pass object default value
        h = self._h if h is None else h
        w = self._w if w is None else w
        return LabelView(self, h, w, y, x)

    def newbox(self, h: int = None, w: int = None, y: int = 0, x: int = 0,
               attr: const.T_COLOR = 0) -> 'BoxView':
        h = self._h if h is None else h
        w = self._w if w is None else w
        return BoxView(self, h, w, y, x, attr)

    def newbutton(self, h: int, w: int, y: int = 0, x: int = 0,
                  text: str = "Button", bid: str = 'b0') -> 'ButtonView':
        return ButtonView(self, h, w, y, x, text, bid)

    def newlist(self, num: int, h: int = None, w: int = None, y: int = 0,
                x: int = 0, margin: int = 0) -> 'ListView':
        h = self._h if h is None else h
        w = self._w if w is None else w
        return ListView(self, num, h, w, y, x, margin)

    def newmap(self, map_data: dict, h: int = None, w: int = None, y: int = 0,
               x: int = 0) -> 'MapView':
        h = self._h if h is None else h
        w = self._w if w is None else w
        return MapView(self, map_data, h, w, y, x)


class BaseWidget(object):

    """A basic widget class"""

    def __init__(self, layout: ViewLayout, h: int, w: int, y: int, x: int):
        """
        :layout: Layout create this widget
        :h: widget height
        :w: widget width
        :y: widget position y
        :x: widget position x
        """
        self._layout = layout
        self._h = h
        self._w = w
        self._y = y
        self._x = x

    @property
    def layout(self):
        return self._layout

    def get_color(self, color: const.T_COLOR) -> int:
        return self.layout.get_color(color)


class Widget(BaseWidget):
    """
    A Widget is a re-usable component that can be used to create a simple GUI.
    """

    def __init__(self, layout: ViewLayout, h: int, w: int, y: int, x: int,
                 pad_h: int = None, pad_w: int = None):
        super().__init__(layout, h, w, y, x)
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
        self.hl_color = const.A_BOLD
        self.hl_mark = const.C_HIGHLIGHT

    def _newpad(self, h: int, w: int):
        # Pad height +1 to fix last space cannot addstr.
        return curses.newpad(h+1, w)

    @property
    def pad(self):
        return self._pad

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

    def addhstr(self, string: str, y: int = 0, x: int = 0, attr: int = 0):
        """Add highlight text"""
        text = string.split(self.hl_mark)
        for i, t in enumerate(text):
            if i == 0:
                self.addstr(y, x, t, attr)
            elif i % 2 == 0:
                self.addstr(t, attr)
            elif i % 2 == 1:
                self.addstr(t, self.hl_color)

    def addwstr(self, string: str, attr: int = 0, v_align: int = 0,
                h_align: int = 0):
        """Add align and hightlight text"""
        lines = _align_text(string, self._h, self._w, v_align, h_align,
                            self.hl_mark)
        for i, text in enumerate(lines):
            self.addhstr(text, i, 0, attr)

    def update(self, pad=None, win=None, pad_y: int = None, pad_x: int = None):
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

    def __init__(self, layout: ViewLayout, h: int, w: int, y: int, x: int):
        # run parent class init function.
        super().__init__(layout, h, w, y, x)
        self._text = 'Lable'
        self._h_align = 0
        self._v_align = 0
        self._attr = 0

    def set_text(self, label: str = None, attr: const.T_COLOR = None,
                 v_align: int = None, h_align: int = None):
        """Set Label text"""
        self._text = self._text if label is None else label
        self._attr = self._attr if attr is None else attr
        self._attr = self.get_color(self._attr)
        self._v_align = self._v_align if v_align is None else v_align
        self._h_align = self._h_align if h_align is None else h_align
        self.pad.clear()
        self.addwstr(self._text, self._attr, self._v_align, self._h_align)


class BoxView(BaseWidget):

    """A simple Box Border and Tile"""

    def __init__(self, layout: ViewLayout, h: int, w: int, y: int, x: int,
                 attr: const.T_COLOR):
        super().__init__(layout, h, w, y, x)
        self._box = self.layout.win.derwin(h, w, y, x)
        self._box.border()
        attr = self.get_color(attr)
        self._box.bkgd(attr)

    def set_title(self, text: str = 'TITLE',
                  attr: const.T_COLOR = const.A_BOLD):
        # Add title
        title_len = len(text) + 2
        self._title = self.layout.newlabel(1, title_len, 0,
                                           int((self._w-title_len)/2))
        self._title.set_text(text, attr, h_align=const.A_CENTER)

    def set_border(self):
        self._box.border()

    def update(self):
        self._title.update()


class ButtonView(LabelView):
    """A simple Button"""

    def __init__(self, layout: ViewLayout, h: int, w: int, y: int, x: int,
                 text: str, bid: str):
        super().__init__(layout, h, w, y, x)
        self._is_focus = False
        self._focus_pad = self._newpad(self._h, self._w)
        self._disabled_pad = self._newpad(self._h, self._w)
        self._bid = bid
        self._is_disabled = False
        self._focus_attr = const.A_REVERSE
        self._disabled_attr = const.A_DIM
        self.set_text(text, h_align=const.A_CENTER)

    @property
    def focus(self):
        return self._is_focus

    @focus.setter
    def focus(self, value):
        if self._is_focus != value:
            self._is_focus = value

    @property
    def disable(self):
        return self._is_disabled

    @disable.setter
    def disable(self, value):
        if self._is_disabled != value:
            self._is_disabled = value

    def update(self, win=None):
        active_pad = self.pad
        if self._is_disabled:
            active_pad = self._disabled_pad
        elif self._is_focus:
            active_pad = self._focus_pad
        super().update(active_pad, win)

    def set_text(self, label: str = None, attr: const.T_COLOR = None,
                 v_align: int = None, h_align: int = None,
                 f_attr: const.T_COLOR = None, d_attr: const.T_COLOR = None):
        super().set_text(label, attr, v_align, h_align)
        self.pad.overwrite(self._focus_pad)
        self.pad.overwrite(self._disabled_pad)
        f_attr = self._focus_attr if f_attr is None else f_attr
        d_attr = self._disabled_attr if d_attr is None else d_attr
        f_attr = self.get_color(f_attr)
        d_attr = self.get_color(d_attr)
        self._focus_pad.bkgd(f_attr)
        self._disabled_pad.bkgd(d_attr)

    def get_text(self):
        return self._text

    def get_id(self):
        return self._bid


class ListView(Widget):
    """A simple List"""

    def __init__(self, layout: ViewLayout, num: int, h: int, w: int, y: int,
                 x: int, margin: int):
        super().__init__(layout, h, w, y, x, num)
        self._list = []
        self._cur_id = 0
        self._len = num
        self._margin = margin
        self._newitem_y = 0
        self._dispal_y = 0

    @property
    def listdrawy(self):
        return self.pad_draw_y

    @listdrawy.setter
    def listdrawy(self, value):
        self.pad_draw_y = value

    @property
    def cur_id(self):
        return self._cur_id

    def _is_valid(self, i_id: int) -> bool:
        if 0 <= i_id < self._newitem_y:
            return True
        else:
            return False

    def add_item(self, label: str = None, attr: const.T_COLOR = None,
                 v_align: int = None, h_align: int = const.A_LEFT,
                 f_attr: const.T_COLOR = None,
                 d_attr: const.T_COLOR = None) -> int:
        if (item_y := self._newitem_y) < self._len:
            newitem = self.layout.newbutton(1, self._w, item_y, 0)
            newitem.set_text(label, attr, v_align, h_align, f_attr, d_attr)
            self._list.append(newitem)
            self._newitem_y += 1
            return item_y
        else:
            return 0

    def get_item(self, i_id: int) -> ButtonView:
        if self._is_valid(i_id):
            return self._list[i_id]
        else:
            return self._list[0]

    def get_cur_item(self):
        return self.get_item(self._cur_id)

    def move_cur(self, i_id: int):
        if self._is_valid(i_id):
            # Hilight cursor
            prev_id = self._cur_id
            self._cur_id = i_id
            self.get_item(prev_id).focus = False
            self.get_cur_item().focus = True
            # Move list
            if self._cur_id > (self.listdrawy + (self._h-1-self._margin)):
                self.move_list(self._cur_id - (self._h-1-self._margin))
            elif self._cur_id < (self.listdrawy + self._margin):
                self.move_list(self._cur_id - self._margin)

    def update(self, i_id: int = const.S_UPDATE_ALL):
        if i_id is const.S_UPDATE_ALL:
            for i in self._list:
                i.update(win=self.pad)
        elif i_id is not const.S_UPDATE_NONE:
            self.get_item(i_id).update(win=self.pad)
        super().update()

    def move_list(self, y: int):
        self.listdrawy = y


class ScrollBarView(Widget):

    """A simple scroll bar"""

    def __init__(self, layout: ViewLayout, h: int, y: int, x: int):
        super().__init__(layout, h, 1, y, x, )
        # self._uparrow_ch = const.C_UPARROW
        # self._downarrow_ch = const.C_DOWNARROW
        # self._slider_ch = const.C_SLIDER

    def set_slider(self, max_len: int, win_h: int):
        ...

    def move_slider(self, pos: int):
        ...


class MapView(Widget):
    """A simple Map"""

    def __init__(self, layout: ViewLayout, map_data: dict, h: int, w: int,
                 y: int, x: int):
        self._map = map_data
        _maph = self._map[const.S_MAP_MAPH]
        _mapw = self._map[const.S_MAP_MAPW]
        super().__init__(layout, h, w, y, x, _maph, _mapw)
        self._cur_gy = 0
        self._cur_gx = 0
        self._grid = []
        self._grid_len = 3
        self._gridh = 0
        self._gridw = 0
        self._layers = []
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
        mapdata = self._map[const.S_MAP_MAP]
        self._margin = self._map[const.S_MAP_MARGIN]
        cells = self._map[const.S_MAP_CELL]
        base_layer = self.add_layer()  # create a base map
        for t in mapdata:
            if (c := cells.get(t, None)):
                color_name = c.get(const.S_MAP_COLOR)
                color = self.get_color(color_name)
                # raise Exception(color, color_name, c)
                map_char = c[const.S_MAP_CHAR]
                base_layer.addch(map_char, color)

    def init_grid(self):
        grid_h = self._map[const.S_MAP_GRIDH]
        grid_w = self._map[const.S_MAP_GRIDW]
        grid_len = self._map.get(const.S_MAP_GRID_LEN,
                                 const.DEF_MAP_GRID_LEN)
        grid_offset = self._map.get(const.S_MAP_GRID_OFFSET,
                                    const.DEF_MAP_GRID_OFFSET)
        grid_space = self._map.get(const.S_MAP_GRID_SPACE,
                                   const.DEF_MAP_GRID_SPACE)
        grid_starty = self._map.get(const.S_MAP_GRIDY, const.DEF_MAP_GRIDY)
        grid_startx = self._map.get(const.S_MAP_GRIDX, const.DEF_MAP_GRIDX)
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

    def update(self, pad=None, win=None, pad_y: int = None, pad_x: int = None,
               all_layers: bool = False):
        if all_layers:
            for layer in self._layers:
                if layer.is_visible:
                    layer.pad.overlay(self.pad)
        super().update(pad, win, pad_y, pad_x)

    def move_map(self, new_y: int, new_x: int):
        self.mapdrawy = new_y
        self.mapdrawx = new_x

    def move_cusor(self, gy: int, gx: int):
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

    def get_grid_yx(self, gy: int, gx: int):
        return self._grid[gy][gx]

    def get_hex(self, gy: int, gx: int):
        result = []
        hex_y, hex_x = self.get_grid_yx(gy, gx)
        for i in range(self._grid_len):
            result.append([self.pad.inch(hex_y, hex_x+i), hex_y, hex_x+i])
        return result

    def set_hex(self):
        ...

    def highlight_hex(self, gy: int, gx: int, is_on: bool):
        hex_data = self.get_hex(gy, gx)
        for h in hex_data:
            hex_d, hex_y, hex_x = h
            hex_attr = chattr(hex_d)
            if is_on:
                attr = hex_attr | const.A_REVERSE
            else:
                attr = hex_attr & ~const.A_REVERSE
            self.pad.chgat(hex_y, hex_x, 1, attr)


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
    ...
