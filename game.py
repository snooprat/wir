#!/usr/bin/env python

# This module starts the game

import curses
import curses.panel as cpanel
import state

class Game:
    """Main game class
    """
    
    def __init__(self):
        """Start game throught curses
        """
        curses.wrapper(self.start)

    def start(self, stdscr):
        state.State(stdscr)
