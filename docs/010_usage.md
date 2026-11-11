# Usage

## From Python

```python
from keybind import KeyBinder


def do():
    print('done')

# The following will start key listening loop in a thread
# (useful if you don't want to block your main program).
KeyBinder.activate({

    'Ctrl-K': do,
    'Shift-R': None,  # Do not run anything, just intercept.

}, run_thread=True)
```

## From CLI

```shell
# Listen to Ctrl-K, Ctrl-R and D (keycode 40).
# Provide as many -k as you want.
$ keybind -k "Ctrl-K=ls -lah" -k "Ctrl-R=python run.py somearg --someopt" -k "40=date"

# All keys interception mode. Show keycodes.
# Use wisely, keep your mouse ready.
$ keybind --sniff
```
