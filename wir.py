#!/usr/bin/env python3
# A curses-based version of War in Russia.

import sys
import curses

import spct


c_hl = {
            'cid': 1,
            'fg': curses.COLOR_YELLOW,
            'bg': curses.COLOR_BLACK,
            'attr': curses.A_BOLD,
        }

l_title = {
            'label': '`War in Russia`\nv0.0.1',
            'v_align': spct.A_MIDDLE,
            'h_align': spct.A_CENTER,
            }


class MainMenuView(spct.Layout):

    def initview(self):
        self.win.addch(curses.ACS_PI)
        self.win.addstr(4, 20, '12345')
        self.win.hline('h', 5)
        self.win.vline('v', 5)


class LogoView(spct.Layout):

    def initview(self):
        self.newbox()
        self.tt = self.newbutton(self._h-2, self._w-2, 1, 1)
        self.tt.hl_color = spct.add_color(**c_hl)
        self.tt.set_text(**l_title)
        self.hide()

    def set_focused(self, is_focused):
        self.tt.set_focused(is_focused)


class MainMenuCtr(spct.ViewController):

    def set_logo(self, logo):
        self.logo = logo

    def on_keypress(self, ch):
        if ch in 'Qq':
            sys.exit()
        if ch == '1':
            self.logo.show()


class LogoCtr(spct.ViewController):

    def set_title(self, title):
        self.title = title

    def on_keypress(self, ch):
        if ch in 'Qq':
            self.hide()
        if ch == '2':
            self.view.set_focused(True)
            # btn1.set_text(h_align=spct.H_LEFT)
        if ch == '3':
            self.view.set_focused(False)
            # btn1.set_text(h_align=spct.H_RIGHT)
        if ch == '4':
            self.title.show()
        spct.update()


def main(stdscr):
    """Game main loop"""
    WIN_H, WIN_W = stdscr.getmaxyx()
    MENU_H = 0
    curses.curs_set(0)
    stdscr.clear()

    titleV = MainMenuView(WIN_H-MENU_H, WIN_W)
    titleC = MainMenuCtr(titleV)
    logoV = LogoView(WIN_H-10, WIN_W-10, 5, 5)
    logoC = LogoCtr(logoV)
    titleC.set_logo(logoC)
    logoC.set_title(titleC)
    spct.update()

    spct.run()


if __name__ == '__main__':
    curses.wrapper(main)
