import pytest
from keybind import KeyBinder, configure_logging


def test_basic(xlib_mock):

    configure_logging()

    xlib_mock.register_events([
        (1, 'K'),
        (1, 'J'),
        (1, 'pass'),  # captured, no handler
        (0, 'pass'),  # non captured
    ])

    pressed = []

    with pytest.raises(IndexError):
        KeyBinder.activate({
            'Ctrl-K': lambda: pressed.append('Ctrl-K'),
            'J': lambda: pressed.append('J'),
            10: lambda: pressed.append('10'),
        })

    # Try bogus grab key.
    xlib_mock.register_error('errr', 'ev')

    with pytest.raises(IndexError):
        KeyBinder.activate({
            'bogus': lambda: None,
        })

    # Try sniffing.
    with pytest.raises(IndexError):
        KeyBinder.activate()


def test_thread(xlib_mock):

    KeyBinder.activate({
        'J': lambda: None,
    }, run_thread=True)
