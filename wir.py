#!/usr/bin/env python3
# A curses-based version of War in Russia.

import spck
import scurses as curses
from spck.view import Layout


def display_menu(stdscr, WINHW):
    WIN_H, WIN_W = WINHW
    MENU_H = 0
    stdscr.clear()

    c_hl = {
        'cid': 1,
        'fg': curses.COLOR_YELLOW,
        'bg': curses.COLOR_BLACK,
        'attr': curses.A_BOLD,
    }

    l_title = {
        'label': '`War in Russia`\nv0.0.1',
        'v_align': spck.V_MIDDLE,
        'h_align': spck.H_CENTER,
    }

    COLOR_HL = spck.add_color(**c_hl)

    title = Layout(WIN_H-MENU_H, WIN_W)
    title.win.addch(curses.ACS_PI)
    title.win.addstr(4, 20, '12345')
    title.win.hline('h', 5)
    title.win.vline('v', 5)
    logo = Layout(WIN_H, WIN_W)
    logo.newbox()
    tt = logo.newlabel(WIN_H-MENU_H-2, WIN_W-2, 1, 1)
    tt.hl_color = COLOR_HL
    tt.update(**l_title)
    btn1 = logo.newbutton(1, 10, WIN_H-1, 10)
    btn1.update('New Game', h_align=spck.H_RIGHT)
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
            if c is '2':
                tt.is_focused = True
                btn1.update(h_align=spck.H_LEFT)
            if c is '3':
                tt.is_focused = False
                btn1.update(h_align=spck.H_RIGHT)
            spck.update()
        else:
            pass

    title.callback_keypress = run
    logo.callback_keypress = logorun
    spck.run()


def main(stdscr):
    """Game main loop"""
    WINHW = stdscr.getmaxyx()

    curses.curs_set(0)
    display_menu(stdscr, WINHW)


if __name__ == '__main__':
    curses.wrapper(main)
