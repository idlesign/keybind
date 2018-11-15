# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import logging
import threading

LOGGER = logging.getLogger('keybinder')


def configure_logging(log_level=None):
    """Performs basic logging configuration.

    :param log_level: logging level, e.g. logging.DEBUG
        Default: logging.INFO

    :param show_logger_names: bool - flag to show logger names in output

    """
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level or logging.INFO)


class KeyBinder(object):
    """Binds keys to functions globally.

        .. code-block:: python

            def do(): print('do')

            KeyBinder.activate({
                'Ctrl-K': do,
            })

    """

    def __init__(self, keymap=None, listen_events=None):
        """
        :param dict keymap: Key name to function mapping.

            Example:

            .. code-block:: python

                def do(): print('do')

                {
                    'Ctrl-K': do,
                    '1': None,  # Just intercept.
                }

        :param int listen_events: X Events or a combination of them.

            Examples:

                * Xlib.X.KeyPressMask
                * Xlib.X.KeyPressMask | Xlib.X.ButtonReleaseMask

        """
        from Xlib import X, XK
        from Xlib.display import Display

        self.x = X
        self.xk = XK
        self.disp = Display()
        self.screen = self.disp.screen().root
        self.events = listen_events or self.x.KeyPressMask

        self.keymap = keymap or {}
        self.mapped = {}

    @classmethod
    def activate(cls, keymap=None, listen_events=None, run_thread=False):
        """Alternative constructor.

        Performs keys binding and runs a listener thread.

        :param dict keymap: Key name to function mapping.

        :param int listen_events: X Events or a combination of them.

        :param bool run_thread: Run a key listening loop in a thread.

        :rtype: KeyBinder

        """
        binder = cls(keymap=keymap, listen_events=listen_events)

        if keymap:
            binder.register_keys()

        else:
            binder.sniff()

        if run_thread:
            binder.run_thread()
        else:
            binder.listen()

        return binder

    def listen(self):
        """Run keys events listening loop."""

        events = self.events
        screen = self.screen
        mapped = self.mapped

        while True:
            event = screen.display.next_event()
            capture = event.type & events

            if not capture:
                continue

            keycode = event.detail

            key, handler = mapped.get(keycode, (keycode, None))

            if handler:
                handler()

            else:
                LOGGER.info('Intercepted key: %s', key)

    def run_thread(self):
        """Runs key events listening loop in a thread."""
        grabber = threading.Thread(target=self.listen)
        grabber.daemon = True
        grabber.start()

    def register_key(self, key, modifier_default='NumLock'):
        """Registers a key to listen to.

        :param str|unicode|int key: Key name or code.

        :param str|unicode modifier_default: Use this modifier if none specified.

        :rtype: bool

        """
        x = self.x

        modifiers = {
            'Ctrl': x.ControlMask,   # 37  105
            'Shift': x.ShiftMask,    # 50  62
            'CapsLock': x.LockMask,  # 66
            'Alt': x.Mod1Mask,       # 64  108
            'NumLock': x.Mod2Mask,   # 77
            'Super': x.Mod4Mask,     # 133  134
        }

        has_error = []

        modifier_alias = None

        if isinstance(key, int):
            keycode = key

        else:
            modifier_alias, _, key_only = key.partition('-')

            if not key_only:
                # Key only, no modifier.
                key_only = modifier_alias
                modifier_alias = None

            keycode = self.disp.keysym_to_keycode(self.xk.string_to_keysym(key_only))

            LOGGER.debug('Key translated: %s -> %s', key, keycode)

        def on_error(err, event):
            has_error.append((err, event))

        modifier_alias = modifier_alias or modifier_default
        modifier = modifiers[modifier_alias]

        # Simulate X.AnyModifier as it leads to BadAccess, as if somebody has already grabbed it before us.
        modifiers_all = [
            modifier,
            modifier | modifiers['NumLock'],
            modifier | modifiers['CapsLock'],
            modifier | modifiers['NumLock'] | modifiers['CapsLock'],
        ]

        for mod in modifiers_all:
            self.screen.grab_key(keycode, mod, True, x.GrabModeAsync, x.GrabModeAsync, on_error)

        success = not has_error

        if success:
            self.mapped[keycode] = (key, self.keymap[key])

        return success

    def register_keys(self):
        """Registers all keys from current keymap."""

        # screen.change_attributes(event_mask=capture_events)

        for key in self.keymap.keys():
            if not self.register_key(key):
                LOGGER.warning('Unable to register handler for: %s', key)

    def sniff(self):
        """Grab all events. Usefull for keycode sniffing."""
        x = self.x
        self.screen.grab_keyboard(self.events, x.GrabModeAsync, x.GrabModeAsync, x.CurrentTime)
