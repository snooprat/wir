#!/usr/bin/env python
# A curses-based version of war in russia.

import curses

import state

def main(stdscr):
    state.State(stdscr)

if __name__ == '__main__':
    curses.wrapper(main)
