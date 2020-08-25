#!/usr/bin/env python3
# A curses-based version of War in Russia.

import sys
import yaml

import spct


l_title = {
    'label': '`W`ar `i`n `R`ussia\nv0.0.1',
    'v_align': spct.AL_MIDDLE,
    'h_align': spct.AL_CENTER,
}


class MainMenuView(spct.ViewLayout):

    def init_view(self):
        self.win.addch('t')
        self.win.addstr(4, 20, '12345')
        self.win.hline('h', 5)
        self.win.vline('v', 5)


class MainMenuCtr(spct.ViewController):

    def set_logo(self, logo):
        self.logo = logo

    def set_map(self, wirmap):
        self.wirmap = wirmap

    def on_event(self, event):
        if event == 'Qq':
            sys.exit("Game exit")
        elif event == '1':
            self.logo.show()
        elif event == '2':
            self.wirmap.show()


class LogoView(spct.ViewLayout):

    def init_view(self):
        self.newbox()
        self.tt = self.newbutton(self.height-2, self.width-2, 1, 1)
        self.tt.hl_color = self.get_color('logo_hl')
        self.tt.set_text(**l_title)
        self.hide()

    def set_focus(self, is_focus):
        self.tt.set_focus(is_focus)


class LogoCtr(spct.ViewController):

    def set_title(self, title):
        self.title = title

    def on_event(self, event):
        if event == 'Qq':
            self.hide()
        elif event == '2':
            self.view.set_focus(True)
            # btn1.set_text(h_align=spct.H_LEFT)
        elif event == '3':
            self.view.set_focus(False)
            # btn1.set_text(h_align=spct.H_RIGHT)
        elif event == spct.KEY_LEFT:
            self.title.show()
        spct.update()


class WIRMapView(spct.ViewLayout):

    def init_view(self):
        with open('map.yml', 'r') as f:
            wirmap = yaml.safe_load(f)
        self.map = self.newmap(wirmap, self.height, self.width)
        self.hide()


class WIRMapCtr(spct.ViewController):

    def on_event(self, event):
        if event == 'Qq':
            self.hide()


def main(stdscr):
    """Game main loop"""
    WIN_H, WIN_W = stdscr.getmaxyx()
    MENU_H = 0
    spct.init()
    with open('color.yml', 'r') as f:
        f_color = yaml.safe_load(f)
    wircolor = spct.ColorMap(f_color)

    titleV = MainMenuView(WIN_H-MENU_H, WIN_W)
    titleC = MainMenuCtr(titleV)
    logoV = LogoView(WIN_H-10, WIN_W-10, 5, 5, colors=wircolor)
    logoC = LogoCtr(logoV)
    mapV = WIRMapView(WIN_H, WIN_W, colors=wircolor)
    mapC = WIRMapCtr(mapV)
    titleC.set_logo(logoC)
    titleC.set_map(mapC)
    logoC.set_title(titleC)
    spct.update()

    spct.run()


if __name__ == '__main__':
    spct.wrapper(main)
