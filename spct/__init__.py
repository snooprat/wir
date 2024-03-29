# A simple py curses toolkit

import sys
import curses
import curses.panel as cpanel

from spct.constant import *
from spct.view import ViewLayout
from spct.viewctr import ViewController
from spct.color import ColorMap, chattr, chcolor, chtext


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


def init_colors(colors: dict) -> ColorMap:
    return ColorMap(colors)


def wrapper(*args, **kwds):
    curses.wrapper(*args, **kwds)
