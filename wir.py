#!/usr/bin/env python3
# A curses-based version of War in Russia.

import sys

import spct
from spct.view import ViewLayout
from spct.controller import ViewController


c_hl = {
            'cid': 1,
            'fg': spct.COLOR_YELLOW,
            'bg': spct.COLOR_BLACK,
            'attr': spct.A_BOLD,
        }

l_title = {
            'label': '`W`ar `i`n `R`ussia\nv0.0.1',
            'v_align': spct.AL_MIDDLE,
            'h_align': spct.AL_CENTER,
            }


class MainMenuView(ViewLayout):

    def init_view(self):
        self.win.addch('t')
        self.win.addstr(4, 20, '12345')
        self.win.hline('h', 5)
        self.win.vline('v', 5)


class LogoView(ViewLayout):

    def init_view(self):
        self.newbox()
        self.tt = self.newbutton(self.height-2, self.width-2, 1, 1)
        self.tt.hl_color = spct.add_color(**c_hl)
        self.tt.set_text(**l_title)
        self.hide()

    def set_focused(self, is_focused):
        self.tt.set_focused(is_focused)


class MainMenuCtr(ViewController):

    def set_logo(self, logo):
        self.logo = logo

    def get_event(self, event):
        if event.is_key('Qq'):
            sys.exit("Game exit")
        if event.is_key('1'):
            self.logo.show()


class LogoCtr(ViewController):

    def set_title(self, title):
        self.title = title

    def get_event(self, event):
        if event.is_key('Qq'):
            self.hide()
        if event.is_key('2'):
            self.view.set_focused(True)
            # btn1.set_text(h_align=spct.H_LEFT)
        if event.is_key('3'):
            self.view.set_focused(False)
            # btn1.set_text(h_align=spct.H_RIGHT)
        if event.is_key(spct.KEY_LEFT):
            self.title.show()
        spct.update()


def main(stdscr):
    """Game main loop"""
    WIN_H, WIN_W = stdscr.getmaxyx()
    MENU_H = 0
    spct.init()

    titleV = MainMenuView(WIN_H-MENU_H, WIN_W)
    titleC = MainMenuCtr(titleV)
    logoV = LogoView(WIN_H-10, WIN_W-10, 5, 5)
    logoC = LogoCtr(logoV)
    titleC.set_logo(logoC)
    logoC.set_title(titleC)
    spct.update()

    spct.run()


if __name__ == '__main__':
    spct.wrapper(main)
