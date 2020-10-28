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

    def on_event(self, event):
        """Overload view on event code"""
        if event == 'Qq':
            sys.exit("User terminated app")

    def show(self):
        self.view.show()

    def hide(self):
        self.view.hide()
