import sys

from spct.event import KeyEvent


class ViewController(object):
    """View Controller control the content of View."""

    def __init__(self, view):
        self.view = view
        self.view.set_ctr(self)

    def on_event(self, event: KeyEvent):
        """Overload view on event code"""
        if event == 'Qq':
            sys.exit("User terminated app")

    def show(self):
        self.view.show()

    def hide(self):
        self.view.hide()
