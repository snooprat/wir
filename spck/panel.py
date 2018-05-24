# scurses panel module.

import spck.unicurses as uc
from spck.scurses import WinObj


global last_panel
last_panel = None


# Panel functions
update_panels = uc.update_panels


def new_panel(win):
    global last_panel
    last_panel = uc.new_panel(win.scr)
    return last_panel


def top_panel():
    global last_panel
    if last_panel:
        while last_panel.above():
            last_panel = last_panel.above()
    return last_panel


def bottom_panel():
    global last_panel
    if last_panel:
        while last_panel.below():
            last_panel = last_panel.below()
    return last_panel


# Functions based on Panel Object
class PanObj(object):
    """Panel object from curses"""
    def __init__(self, panel):
        self.panel = panel

    def __del__(self):
        return uc.del_panel(self.panel)

    def above(self, *args, **kwds):
        return uc.panel_above(self.panel, *args, **kwds)

    def below(self, *args, **kwds):
        return uc.panel_below(self.panel, *args, **kwds)

    def bottom(self, *args, **kwds):
        return uc.bottom_panel(self.panel, *args, **kwds)

    def hidden(self, *args, **kwds):
        return uc.panel_hidden(self.panel, *args, **kwds)

    def hide(self, *args, **kwds):
        return uc.hide_panel(self.panel, *args, **kwds)

    def move(self, *args, **kwds):
        return uc.move_panel(self.panel, *args, **kwds)

    def replace(self, win):
        return uc.replace_panel(self.panel, win.scr)

    def set_userptr(self, *args, **kwds):
        return uc.set_panel_userptr(self.panel, *args, **kwds)

    def show(self, *args, **kwds):
        return uc.show_panel(self.panel, *args, **kwds)

    def top(self, *args, **kwds):
        return uc.top_panel(self.panel, *args, **kwds)

    def userptr(self, *args, **kwds):
        return uc.panel_userptr(self.panel, *args, **kwds)

    def window(self, *args, **kwds):
        return WinObj(uc.panel_window(self.panel, *args, **kwds))
