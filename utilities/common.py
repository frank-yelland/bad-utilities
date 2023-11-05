"""common - mostly just error warning and debug printing for now

Copyright 2023 Frank Yelland

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

_ansi_commands = {
    "reset_style": "\x1b[0m",
    "bold": "\x1b[1m",
    "bold_reset": "\x1b[22m",
    "dim": "\x1b[2m",
    "dim_reset": "\x1b[22m",
    "italic": "\x1b[3m",
    "italic_reset": "\x1b[23m",
    "strike": "\x1b[9m",
    "strike_reset": "\x1b[29m",
    "clear": "\x1bc",
    "clear_line": "\x1b[2K",
    "goto": "\x1b[{};{}H",
    "mv_up": "\x1b[{}A",
    "mv_lt": "\x1b[{}D",
    "mv_rt": "\x1b[{}C",
    "mv_dn": "\x1b[{}B",
    "save_cur_pos": "\x1b[s",
    "load_cur_pos": "\x1b[u",
}


def print_warning(*strings: str, line_end: str = "\n"):
    """prints a warning message to the console
    arguments:
        *strings: str; warnings to print
    optional arguments:
        line_end; str, line ending to use"""
    for string in strings:
        print(f"{colour(220)}[WARNING]: {string}{colour(-1)}", end=line_end)


def print_error(*strings: str, line_end: str = "\n"):
    """prints a error message to the console
    arguments:
        *strings: str; warnings to print
    optional arguments:
        line_end; str, line ending to use"""
    for string in strings:
        print(f"{colour(196)}[ERROR]: {string}{colour(-1)}", end=line_end)


def print_info(*strings: str, line_end: str = "\n"):
    """prints a informational message to the console
    arguments:
        *strings: str; warnings to print
    optional arguments:
        line_end; str, line ending to use"""
    for string in strings:
        print(f"{colour(27)}[INFO]: {string}{colour(-1)}", end=line_end)


def colour(colour_id: int, background: bool = False) -> str:
    """retuns the ansi colour code for a given colour, see
    https://user-images.githubusercontent.com/995050/47952855-ecb12480-df75-11e8-89d4-ac26c50e80b9.png
    for a table of colours
    arguments:
        colour_id: int; id of 256-colour terminal colour, and -1 for reset
        background: bool; whether the colour is background or not
    returns:
        colour_code: str; ansi colour code, and a blank string
                     if the colour is not found"""
    if isinstance(colour_id, int):
        if colour_id == -1:
            return "\x1b[0m"
        colour_id %= 256
        if background:
            return f"\x1b[48;5;{colour_id}m"
        else:
            return f"\x1b[38;5;{colour_id}m"


def cmd(command: str, *args) -> str:
    """returns an ansi terminal command
    arguments:
        command: str; name of commnad
    returns:
        command_string: str; console code of command"""
    if command in _ansi_commands:
        return _ansi_commands[command].format(*args)
    else:
        return ""
