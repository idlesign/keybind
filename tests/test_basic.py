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


@pytest.mark.parametrize("key_input, expected_result",
        [
            ("J", ([], "J")),
            ("Ctrl-J", (["Ctrl"], "J")),
            ("Ctrl-Alt-J", (["Ctrl", "Alt"], "J")),
            ("", ([], "")),
        ]
    )
def test_parse_key_valid_input(key_input, expected_result, xlib_mock):
    # GIVEN valid input describing a key or key combination

    # WHEN the input is parsed
    binder = KeyBinder()

    # THEN the expected result is returned
    assert binder._parse_key(key_input) ==  expected_result


def test_parse_key_invalid_input(xlib_mock):
    # GIVEN a list of valid input types and input that is not one of those
    valid_input_types = [str, int]

    invalid_input = ["Ctrl", "J"]

    assert type(invalid_input) not in valid_input_types

    # WHEN the input gets parsed
    binder = KeyBinder()

    # THEN a TypeError is raised
    with pytest.raises(TypeError):
        binder._parse_key(invalid_input)

