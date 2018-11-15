keybind
=======
https://github.com/idlesign/keybind

|release| |lic|

.. |release| image:: https://img.shields.io/pypi/v/keybind.svg
    :target: https://pypi.python.org/pypi/keybind

.. |lic| image:: https://img.shields.io/pypi/l/keybind.svg
    :target: https://pypi.python.org/pypi/keybind


Description
-----------

*Global key binding made easy*

**Requires X11 (X Window System). For UNIX-like systems, e.g. Linux.**

Can be used both as a Python package and from CLI.

Features:

    * Create some global key bindings to your functions.
    * Use them in your GUI or CLI application.
    * Bind arbitrary program run to a key using CLI.


From Python
~~~~~~~~~~~

.. code-block:: python

    from keybinder import KeyBinder


    def do():
        print('done')

    # The following will start key listening loop in a thread
    # (useful if you don't want to block your main program).
    KeyBinder.activate({

        'Ctrl-K': do,
        'Shift-R': None,  # Do not run anything, just intercept.

    }, run_thread=True)



From CLI
~~~~~~~~

.. code-block:: bash

    ; Listen to Ctrl-K and Ctrl-D.
    ; Provide as many -k as you want.
    $ keybind -k "Ctrl-K=ls -lah" -k "Ctrl-D=python run.py somearg --someopt"

    ; All keys interception mode. Show keycodes.
    ; Use wisely, keep your mouse ready.
    $ keybind

