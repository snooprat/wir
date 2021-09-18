import curses
from typing import Union

import spct.constant as const


def chattr(ch: int) -> int:
    return ch & const.A_ATTRIBUTES


def chcolor(ch: int) -> int:
    return ch & const.A_COLOR


def chtext(ch: int) -> int:
    return ch & const.A_CHARTEXT


class ColorMap(object):
    """Manage colors"""

    def __init__(self, colors: dict = None):
        self._cid = 1
        self._colors = {}
        self._attr = {
            const.S_A_BLINK: const.A_BLINK,
            const.S_A_BOLD: const.A_BOLD,
            const.S_A_DIM: const.A_DIM,
            const.S_A_NORMAL: const.A_NORMAL,
            const.S_A_REVERSE: const.A_REVERSE,
            const.S_A_STANDOUT: const.A_STANDOUT,
            const.S_A_UNDERLINE: const.A_UNDERLINE
        }
        self.add_color(const.S_COLOR_DEFAULT)
        self.add_color_map(colors)

    def add_color(self, sel: str, fg: int = const.COLOR_WHITE,
                  bg: int = const.COLOR_BLACK,
                  attr: int = const.A_NORMAL) -> int:
        curses.init_pair(self._cid, fg, bg)
        self._colors[sel] = curses.color_pair(self._cid) | attr
        self._cid += 1
        return self._colors[sel]

    def add_color_map(self, colors: Union[dict, None]):
        if colors:
            for k, v in colors.items():
                fg = v.get(const.S_COLOR_FG, const.COLOR_WHITE)
                bg = v.get(const.S_COLOR_BG, const.COLOR_BLACK)
                attr = self.get_attr(v.get(const.S_COLOR_ATTR))
                self.add_color(k, fg, bg, attr)

    def get_attr(self, attr: str) -> int:
        return self._attr.get(attr, const.A_NORMAL)

    def get_color(self, sel: str = const.S_COLOR_DEFAULT) -> int:
        return self._colors.get(sel, self._colors[const.S_COLOR_DEFAULT])
