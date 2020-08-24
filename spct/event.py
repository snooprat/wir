class Event(object):
    """A class to hold information about a input event."""


class KeyEvent(Event):
    """ This event represents a key press."""

    def __init__(self, key_code):
        self.key_code = key_code

    def __repr__(self):
        return "Keyboard Event: {}".format(self.key_code)

    def __eq__(self, other):
        return self.is_key(other)

    def is_key(self, ch):
        if isinstance(ch, str):
            if chr(self.key_code) in ch:
                return True
            else:
                return False
        elif isinstance(ch, int):
            if self.key_code == ch:
                return True
            else:
                return False
        else:
            raise Exception("KeyEvent type error: neither int nor str", ch)
