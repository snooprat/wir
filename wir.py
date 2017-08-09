#!/usr/bin/env python3
# A curses-based version of war in russia.

import curses
import spck


def display_menu(stdscr, WINHW):
    WIN_H, WIN_W = WINHW
    MENU_H = 0
    stdscr.clear()

    COLOR_HL = spck.add_color(
        1,
        curses.COLOR_YELLOW,
        curses.COLOR_BLACK,
        curses.A_BOLD)

    title = spck.Layout(WIN_H-MENU_H, WIN_W)
    title.win.addch(curses.ACS_PI)
    title.win.addstr(4, 20, '12345')
    title.win.hline('h', 5)
    title.win.vline('v', 5)
    # title.newlabel('War in Russia\nv0.0.1')
    logo = spck.Layout(WIN_H, WIN_W)
    bg = logo.newlabel(WIN_H, WIN_W)
    bg.win.border()
    tt = logo.newlabel(WIN_H-MENU_H-2, WIN_W-2, 1, 1)
    tt.hl_color = COLOR_HL
    tt.update(
        '`War in Russia`\nv0.0.1',
        v_align=spck.V_MIDDLE,
        h_align=spck.H_CENTER)
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
            if c is '3':
                tt.is_focused = False
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
