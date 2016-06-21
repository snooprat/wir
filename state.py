#!/usr/bin/env python

import curses
import curses.panel as cpanel


class State(object):
    """Game state class
    """

    def __init__(self, stdscr):
        """State class initialization
        """
        self.stdscr = stdscr
        self.start()

    def start(self):
        """Initialize the game
        """
        stdscr = self.stdscr
        curses.curs_set(0)

        self.WINHW = (stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 3)
        self.cur = [0, 0]
        self.mapscr = [0, 0]
        self.MAPHW = (99, 99)

        map = curses.newpad(self.MAPHW[0]+1, self.MAPHW[1]+1)

        # curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
        # CP_FWHITE_BGRAY = curses.color_pair(1) | curses.A_REVERSE | curses.A_BOLD
        CP1 = curses.color_pair(1)
        CP2 = curses.color_pair(2)
        CP3 = curses.color_pair(3)
        for y in range(0, self.MAPHW[0]):
            for x in range(0, self.MAPHW[1]+1):
                # map.addch(y, x, random.randint(32, 122))
                # if ((x + (y%2) + 2) / 2) % 2:
                #     map.addch(y, x, '.', CP_FWHITE_BGRAY)
                # else: 
                #     map.addch(y, x, '.')
                # grid = ((x + (y%2)*3) / 2) % 3
                grid = (x + (y%2)*2) % 4
                if grid == 3:
                    map.addch(y, x, ' ')
                # elif grid == 0:
                #     map.addch(y, x, '.')
                else:
                    map.addch(y, x, ':')
                # elif grid == 1:
                #     map.addch(y, x, '.')
                # elif grid == 2:
                #     map.addch(y, x, '.')
                self.map = map

        dia = curses.newwin(3, 20, self.WINHW[0]/2, (self.WINHW[1]-20)/2)
        dia.border()
        dia.addstr(1, 4, 'Hello World!')
        dia2 = curses.newwin(5,5,11,40)
        dia2.border()
        self.dia = dia
        self.dia2 = dia2

        self.pdia = cpanel.new_panel(dia)
        self.p2 = cpanel.new_panel(dia2)
        cpanel.update_panels()
        curses.doupdate()

        self._draw_cur()
        # stdscr.refresh()
        self._draw_map()
        self.run()

    def run(self):
        """Main game loop
        """
        while True:
            ch = self.stdscr.getch()
            if ch == ord('q'):
                break
            elif ch == curses.KEY_UP:
                self._move_cur(0)
            elif ch == curses.KEY_DOWN:
                self._move_cur(1)
            elif ch == curses.KEY_LEFT:
                self._move_cur(2)
            elif ch == curses.KEY_RIGHT:
                self._move_cur(3)
            elif ch == ord('1'):
                if not self.pdia.hidden(): self.pdia.hide()
                else: self.pdia.show()
                # self.p2.move(11, self.dia2.getbegyx()[1] - 1)
                self._draw_map()
            elif ch == ord('`'):
                del self.p2
                del self.pdia
                self._draw_map()
                raise Exception(cpanel.top_panel())

            elif ch == ord('2'):
                self.map.addstr(self.cur[0], self.cur[1], '~~', curses.color_pair(1))
                self._clear_cur()
            elif ch == ord('3'):
                self.map.addstr(self.cur[0], self.cur[1], '..', curses.color_pair(2))
                self._clear_cur()
            elif ch == ord('4'):
                self.map.addstr(self.cur[0], self.cur[1], '^^', curses.color_pair(3))
                self._clear_cur()
            elif ch == ord('5'):
                self.map.addstr(self.cur[0], self.cur[1], '  ', curses.color_pair(0))
                self._clear_cur()

    def _draw_cur(self):
        attr = self.map.inch(self.cur[0], self.cur[1]) & curses.A_ATTRIBUTES
        self.map.chgat(self.cur[0], self.cur[1], 3, attr | curses.A_REVERSE)

    def _draw_map(self):
        # self.map.refresh(self.mapscr[0], self.mapscr[1], 0, 0, *self.WINHW)
        self.map.overwrite(self.stdscr, self.mapscr[0], self.mapscr[1], 0, 0, *self.WINHW)
        cpanel.update_panels()
        curses.doupdate()

    def _clear_cur(self):
        attr = self.map.inch(self.cur[0], self.cur[1]) & curses.A_ATTRIBUTES
        self.map.chgat(self.cur[0], self.cur[1], 3, attr ^ curses.A_REVERSE)

    def _move_cur(self, dir):
        if self.mapscr[1] <= self.cur[1] <= self.mapscr[1] + self.WINHW[1]:
            if dir in (0, 2):
                i = dir / 2
                if self.mapscr[i] < self.cur[i] and self.cur[i] >= 1 + dir / 2:
                    self._clear_cur()
                    self.cur[i] -= 1 + dir / 2*3
                    if dir == 0:
                        if self.cur[i] % 2:
                            self.cur[1] += 2
                        else: self.cur[1] -=2
                    self._draw_cur()
                elif self.cur[i] == self.mapscr[i] and self.mapscr[i] > 0:
                    self.mapscr[i] -= 1 + dir / 2*3
                    self._clear_cur()
                    self.cur[i] -= 1 + dir / 2*3
                    if dir == 0:
                        if self.cur[i] % 2:
                            self.cur[1] += 2
                        else: self.cur[1] -=2
                    self._draw_cur()
            elif dir in (1, 3):
                i = dir / 2
                if self.cur[i] < self.mapscr[i] + self.WINHW[i] - 1:
                    self._clear_cur()
                    self.cur[i] += 1 + dir / 2*3
                    if dir == 1:
                        if self.cur[i] % 2:
                            self.cur[1] += 2
                        else: self.cur[1] -=2
                    self._draw_cur()
                elif self.cur[i] == self.mapscr[i] + self.WINHW[i] - 1 and self.mapscr[i] + self.WINHW[i] < self.MAPHW[i]:
                    self.mapscr[i] += 1 + dir / 2*3
                    self._clear_cur()
                    self.cur[i] += 1 + dir / 2*3
                    if dir == 1:
                        if self.cur[i] % 2:
                            self.cur[1] += 1
                        else: self.cur[1] -=1
                    self._draw_cur()
            self._draw_map()


class MainMenu(State):
    """Game main menu
    """
    pass

class GameMap(State):
    """Game running screen
    """
    pass

