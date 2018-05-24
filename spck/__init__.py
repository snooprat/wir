# A simple py curses toolkit

import spck.scurses as curses
import spck.panel as cpanel

# Constants
V_TOP = 1
V_MIDDLE = 2
V_BOTTOM = 3
H_LEFT = 4
H_CENTER = 5
H_RIGHT = 6

IGNORE_CH = '`'


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
        top_layout = cpanel.top_panel().userptr()
        ch = top_layout.win.getch()
        top_layout.on_keypress(ch)
