#!/usr/bin/env python3
# A curses-based version of War in Russia.

import spct
from spct.view import Layout

import curses


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
        'v_align': spct.V_MIDDLE,
        'h_align': spct.H_CENTER,
    }

    COLOR_HL = spct.add_color(**c_hl)

    title = Layout(WIN_H-MENU_H, WIN_W)
    title.win.addch(curses.ACS_PI)
    title.win.addstr(4, 20, '12345')
    title.win.hline('h', 5)
    title.win.vline('v', 5)
    logo = Layout(WIN_H, WIN_W)
    logo.newbox()
    tt = logo.newbutton(WIN_H-MENU_H-2, WIN_W-2, 1, 1)
    tt.hl_color = COLOR_HL
    tt.set_text(**l_title)
    # btn1 = logo.newbutton(1, 10, WIN_H-1, 10)
    # btn1.set_text('New Game')
    logo.hide()
    spct.update()

    def run(ch):
        if 0 < ch < 256:
            c = chr(ch)
            if c in 'Qq':
                exit()
            if c == '1':
                logo.show()
        else:
            pass

    def logorun(ch):
        if 0 < ch < 256:
            c = chr(ch)
            if c in 'Qq':
                logo.hide()
            if c == '2':
                tt.set_focused(True)
                # btn1.set_text(h_align=spct.H_LEFT)
            if c == '3':
                tt.set_focused(False)
                # btn1.set_text(h_align=spct.H_RIGHT)
            spct.update()
        else:
            pass

    title.callback_keypress = run
    logo.callback_keypress = logorun


def main(stdscr):
    """Game main loop"""
    WINHW = stdscr.getmaxyx()
    curses.curs_set(0)

    display_menu(stdscr, WINHW)
    spct.run()


if __name__ == '__main__':
    curses.wrapper(main)
