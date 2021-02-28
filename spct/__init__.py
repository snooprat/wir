# A simple py curses toolkit

import sys
import curses
import curses.panel as cpanel

from spct.constant import *
from spct.view import ViewLayout
from spct.viewctr import ViewController


class ColorMap(object):
    """Manage colors"""

    def __init__(self, colors=None):
        self._cid = 1
        self._colors = {}
        self._attr = {
            CH_A_BOLD: A_BOLD,
            CH_A_NORMAL: A_NORMAL,
            CH_A_REVERSE: A_REVERSE,
            CH_A_UNDERLINE: A_UNDERLINE
        }
        self.add_color(CH_COLOR_DEFAULT)
        self.add_color_map(colors)

    def add_color(self, sel, fg=COLOR_WHITE, bg=COLOR_BLACK, attr=A_NORMAL):
        curses.init_pair(self._cid, fg, bg)
        self._colors[sel] = curses.color_pair(self._cid) | attr
        self._cid += 1
        return self._colors[sel]

    def add_color_map(self, colors):
        if colors:
            for k, v in colors.items():
                fg = v.get(CH_COLOR_FG, COLOR_WHITE)
                bg = v.get(CH_COLOR_BG, COLOR_BLACK)
                attr = self.get_attr(v.get(CH_COLOR_ATTR))
                self.add_color(k, fg, bg, attr)

    def get_attr(self, attr):
        return self._attr.get(attr, A_NORMAL)

    def get_color(self, sel=CH_COLOR_DEFAULT):
        return self._colors.get(sel, self._colors[CH_COLOR_DEFAULT])


def update():
    """Update screen display"""
    cpanel.update_panels()
    curses.doupdate()


def run():
    """Run the top layout's function."""
    while True:
        try:
            top_layout = cpanel.top_panel().userptr()
            top_layout.run_ctr()
        except AttributeError:
            sys.exit("Please create at least one view layout.")


def init():
    curses.curs_set(0)


def wrapper(*args, **kwds):
    curses.wrapper(*args, **kwds)
