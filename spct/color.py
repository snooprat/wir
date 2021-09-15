import curses
from typing import Union

import spct.constant as CONST


def chattr(ch: int) -> int:
    return ch & CONST.A_ATTRIBUTES


def chcolor(ch: int) -> int:
    return ch & CONST.A_COLOR


def chtext(ch: int) -> int:
    return ch & CONST.A_CHARTEXT


class ColorMap(object):
    """Manage colors"""

    def __init__(self, colors: dict = None):
        self._cid = 1
        self._colors = {}
        self._attr = {
            CONST.S_A_BLINK: CONST.A_BLINK,
            CONST.S_A_BOLD: CONST.A_BOLD,
            CONST.S_A_DIM: CONST.A_DIM,
            CONST.S_A_NORMAL: CONST.A_NORMAL,
            CONST.S_A_REVERSE: CONST.A_REVERSE,
            CONST.S_A_STANDOUT: CONST.A_STANDOUT,
            CONST.S_A_UNDERLINE: CONST.A_UNDERLINE
        }
        self.add_color(CONST.S_COLOR_DEFAULT)
        self.add_color_map(colors)

    def add_color(self, sel: str, fg: int = CONST.COLOR_WHITE,
                  bg: int = CONST.COLOR_BLACK,
                  attr: int = CONST.A_NORMAL) -> int:
        curses.init_pair(self._cid, fg, bg)
        self._colors[sel] = curses.color_pair(self._cid) | attr
        self._cid += 1
        return self._colors[sel]

    def add_color_map(self, colors: Union[dict, None]):
        if colors:
            for k, v in colors.items():
                fg = v.get(CONST.S_COLOR_FG, CONST.COLOR_WHITE)
                bg = v.get(CONST.S_COLOR_BG, CONST.COLOR_BLACK)
                attr = self.get_attr(v.get(CONST.S_COLOR_ATTR))
                self.add_color(k, fg, bg, attr)

    def get_attr(self, attr: str) -> int:
        return self._attr.get(attr, CONST.A_NORMAL)

    def get_color(self, sel: str = CONST.S_COLOR_DEFAULT) -> int:
        return self._colors.get(sel, self._colors[CONST.S_COLOR_DEFAULT])
