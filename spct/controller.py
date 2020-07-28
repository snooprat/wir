import sys


class ViewController(object):
    """View Controller control the content of View."""

    def __init__(self, view):
        self._view = None
        self.view = view

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, view):
        self._view = view
        self.view.viewctr = self

    def on_keypress(self, ch):
        if ch in (ord('Q'), ord('q')):
            sys.exit("User terminated app")

    def show(self):
        self.view.show()

    def hide(self):
        self.view.hide()
