# scurses panel module.

import spck.unicurses as uc


# Panel functions
update_panels = uc.update_panels


global last_panel
last_panel = None


def new_panel(win):
    global last_panel
    np = uc.new_panel(win.scr)
    last_panel = PanObj(np, win)
    uc.set_panel_userptr(np, last_panel)
    return last_panel


def top_panel():
    global last_panel
    tp = last_panel
    while tp and tp.above():
        tp = tp.above()
    return tp


def bottom_panel():
    global last_panel
    bp = last_panel
    while bp and bp.below():
        bp = bp.below()
    return bp


# Functions based on Panel Object
class PanObj(object):
    """Panel object from curses"""
    def __init__(self, panel, win):
        self.panel = panel
        self._win = win
        self._userptr = None

    def __del__(self):
        return uc.del_panel(self.panel)

    def above(self, *args, **kwds):
        pa = uc.panel_above(self.panel, *args, **kwds)
        if pa is None:
            return None
        else:
            return uc.panel_userptr(pa)

    def below(self, *args, **kwds):
        pb = uc.panel_below(self.panel, *args, **kwds)
        if pb is None:
            return None
        else:
            return uc.panel_userptr(pb)

    def bottom(self, *args, **kwds):
        return uc.bottom_panel(self.panel, *args, **kwds)

    def hidden(self, *args, **kwds):
        return uc.panel_hidden(self.panel, *args, **kwds)

    def hide(self, *args, **kwds):
        global last_panel
        if self.above():
            last_panel = self.above()
        elif self.below():
            last_panel = self.below()
        else:
            last_panel = None
        return uc.hide_panel(self.panel, *args, **kwds)

    def move(self, *args, **kwds):
        return uc.move_panel(self.panel, *args, **kwds)

    def replace(self, win):
        return uc.replace_panel(self.panel, win.scr)

    def set_userptr(self, obj):
        self._userptr = obj

    def show(self, *args, **kwds):
        global last_panel
        last_panel = self
        return uc.show_panel(self.panel, *args, **kwds)

    def top(self, *args, **kwds):
        return uc.top_panel(self.panel, *args, **kwds)

    def userptr(self):
        return self._userptr

    def window(self):
        return self._win
