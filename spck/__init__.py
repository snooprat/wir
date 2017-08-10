# A simple py curses toolkit

import curses
import curses.panel as cpanel

# Constants
V_TOP = 1
V_MIDDLE = 2
V_BOTTOM = 3
H_LEFT = 4
H_CENTER = 5
H_RIGHT = 6

IGNORE_CH = '`'

_C_ID = 'id'
_C_FG = 'fg'
_C_BG = 'bg'
_C_ATTR = 'attr'


def add_color(color):
    color_number = color.get(_C_ID)
    fg = color.get(_C_FG) if color.get(_C_FG) else curses.COLOR_WHITE
    bg = color.get(_C_BG) if color.get(_C_BG) else curses.COLOR_BLACK
    attr = color.get(_C_ATTR) if color.get(_C_ATTR) else curses.A_NORMAL
    curses.init_pair(color_number, fg, bg)
    return curses.color_pair(color_number) | attr


def update():
    """Update screen display"""
    top_layout = curses.panel.top_panel().userptr()
    top_layout.refresh()
    cpanel.update_panels()
    curses.doupdate()


def run():
    """Run the top layout's function."""
    while True:
        top_layout = curses.panel.top_panel().userptr()
        ch = top_layout.win.getch()
        top_layout.on_keypress(ch)
