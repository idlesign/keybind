from collections import namedtuple, deque

import pytest


@pytest.fixture
def xlib_mock(stub):

    class X:
        GrabModeAsync = 'asy'
        CurrentTime = 'cut'

        KeyPressMask = 1
        ControlMask = 2
        ShiftMask = 3
        LockMask = 4
        Mod1Mask = 5
        Mod2Mask = 6
        Mod4Mask = 7

    class XK:

        @classmethod
        def string_to_keysym(cls, k):
            return k

    class Screen:

        @property
        def root(self):
            return Screen()

        @property
        def display(self):
            return display

        def grab_key(self, keycode, mod, flag, asy1, asy2, on_error):
            try:
                err = reg_error.pop()
                on_error(*err)
            except IndexError:
                pass

        def grab_keyboard(self, events, asy1, asy2, time):
            return

    Event = namedtuple('Event', ['type', 'detail'])

    class Display:

        def __init__(self):
            self.events = deque()

        def register_events(self, events):
            self.events.clear()
            for type, detail in events:
                self.events.append(Event(type, detail))

        def register_error(self, err, event):
            reg_error.append((err, event))

        def next_event(self):
            return self.events.popleft()

        def keysym_to_keycode(self, ksym):
            return ksym

        def screen(self):
            return Screen()

    x = X
    xk = XK
    display = Display()
    reg_error = []

    stub.apply({
        'Xlib': {
            'X': x,
            'XK': xk,
        },
        'Xlib.display.Display': Display,
    })

    return display
