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
        self.win.vline('a', 5)


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


class LogoCtr(spct.ViewController):

    def set_title(self, title):
        self.title = title

    def on_event(self, event):
        if event == 'Qq':
            self.hide()
        elif event == '2':
            self.view.tt.focus = True
            # btn1.set_text(h_align=spct.H_LEFT)
        elif event == '3':
            self.view.tt.focus = False
            # btn1.set_text(h_align=spct.H_RIGHT)
        elif event == spct.KEY_LEFT:
            self.title.show()
        spct.update()


class WIRMapView(spct.ViewLayout):

    def init_view(self):
        with open('map.yml', 'r') as f:
            wirmap = yaml.safe_load(f)
        self.map = self.newmap(wirmap, self.height, self.width)
        self.layer_unit = self.map.add_layer()
        self.layer_unit.addstr(5, 18, '[X]', self.get_color('unit1'))
        self.map.update(all_layers=True)
        self.hide()

    def move(self, new_y, new_x):
        self.map.move_map(new_y, new_x)
        self.map.update()

    def move_cusor(self, new_gy, new_gx):
        self.map.move_cusor(new_gy, new_gx)
        self.map.update()


class WIRMapCtr(spct.ViewController):

    def on_event(self, event):
        if event == 'Qq':
            self.hide()
        if event == spct.KEY_LEFT:
            self.view.move_cusor(self.view.map.cur_gy, self.view.map.cur_gx-1)
        if event == spct.KEY_RIGHT:
            self.view.move_cusor(self.view.map.cur_gy, self.view.map.cur_gx+1)
        if event == spct.KEY_UP:
            self.view.move_cusor(self.view.map.cur_gy-1, self.view.map.cur_gx)
        if event == spct.KEY_DOWN:
            self.view.move_cusor(self.view.map.cur_gy+1, self.view.map.cur_gx)


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
