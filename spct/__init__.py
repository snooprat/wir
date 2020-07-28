# A simple py curses toolkit

import sys
import curses
import curses.panel as cpanel


# CONSTANT

# Align code
A_TOP = 1
A_MIDDLE = 2
A_BOTTOM = 3
A_LEFT = 4
A_CENTER = 5
A_RIGHT = 6

# Special character
CH_HIGHLIGHT = '`'

from spct.view import Layout
from spct.controller import ViewController


def add_color(cid, fg=curses.COLOR_WHITE, bg=curses.COLOR_BLACK,
              attr=curses.A_NORMAL):
    curses.init_pair(cid, fg, bg)
    return curses.color_pair(cid) | attr


def update():
    """Update screen display"""
    cpanel.update_panels()
    curses.doupdate()


def run():
    """Run the top layout's function."""
    while True:
        try:
            top_layout = cpanel.top_panel().userptr()
        except AttributeError:
            sys.exit("Please create at least one layout.")
        top_layout.run_ctr()
