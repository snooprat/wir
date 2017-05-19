#!/usr/bin/env python3
# A curses-based version of war in russia.

import curses
import curses.panel as cpanel
import spck


def display_menu(stdscr, WINHW):
    WIN_H, WIN_W = WINHW
    MENU_H = 0
    stdscr.clear()

    title = spck.Layout(WIN_H-MENU_H, WIN_W)
    title.addch(curses.ACS_PI)
    title.addstr('12345', y=4, x=20)
    title.hline('h', 5)
    title.vline('v', 5)
    #title.newlabel('War in Russia\nv0.0.1')
    logo = spck.Layout(WIN_H, WIN_W)
    bg = logo.newlabel('', WIN_H, WIN_W, 0, 0)
    bg.border()
    logo.newlabel('War in Russia\nv0.0.1', WIN_H-MENU_H-2, WIN_W-2, 1, 1)
    logo.hide()
    spck.update()

    def run(ch):
        if 0 < ch < 256:
            c = chr(ch)
            if c in 'Qq':
                exit()
            if c is '1':
                logo.show()
        else:
            pass

    def logorun(ch):
        if 0 < ch < 256:
            c = chr(ch)
            if c in 'Qq':
                logo.hide()
        else:
            pass

    title.set_keyfunc(run)
    logo.set_keyfunc(logorun)
    spck.run()

def main(stdscr):
    """Game main loop"""
    WINHW = stdscr.getmaxyx()

    curses.curs_set(0)
    display_menu(stdscr, WINHW)


if __name__ == '__main__':
    curses.wrapper(main)
