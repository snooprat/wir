# scurses panel module.

import scurses.unicurses as uc


# Panel functions
update_panels = uc.update_panels


global _top_panel
_top_panel = None


def new_panel(win):
    np = PanObj(uc.new_panel(win.scr), win)
    np.top()
    return np


def _set_top_panel(panel):
    global _top_panel
    _top_panel = panel


def top_panel():
    global _top_panel
    return _top_panel


def bottom_panel():
    bp = top_panel()
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
        self._above = None
        self._below = None

    def __del__(self):
        return uc.del_panel(self.panel)

    def _set_above(self, panel):
        self._above = panel

    def _set_below(self, panel):
        self._below = panel

    def _remove(self):
        if self == top_panel() and self.below():
            _set_top_panel(self.below())
        if self.above():
            self.above()._set_below(self.below())
        if self.below():
            self.below()._set_above(self.above())

    def above(self):
        return self._above

    def below(self):
        return self._below

    def bottom(self, *args, **kwds):
        bp = bottom_panel()
        if bp and bp != self:
            self._remove()
            bp._set_below(self)
            self._set_above(bp)
        return uc.bottom_panel(self.panel, *args, **kwds)

    def hidden(self, *args, **kwds):
        return uc.panel_hidden(self.panel, *args, **kwds)

    def hide(self, *args, **kwds):
        self._remove()
        return uc.hide_panel(self.panel, *args, **kwds)

    def move(self, *args, **kwds):
        return uc.move_panel(self.panel, *args, **kwds)

    def replace(self, win):
        return uc.replace_panel(self.panel, win.scr)

    def set_userptr(self, obj):
        self._userptr = obj

    def show(self, *args, **kwds):
        self.top()
        return uc.show_panel(self.panel, *args, **kwds)

    def top(self, *args, **kwds):
        tp = top_panel()
        if tp and tp != self:
            self._remove()
            tp._set_above(self)
            self._set_below(tp)
        _set_top_panel(self)
        return uc.top_panel(self.panel, *args, **kwds)

    def userptr(self):
        return self._userptr

    def window(self):
        return self._win
