#!/usr/bin/python3

"""webp find and destroy: searches for and converts webp
files to pngs

Copyright (c) 2023 sjvadstik3

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import os
import re
import sys

try:
    from PIL import Image
except ModuleNotFoundError:
    print("PIL is not installed - you need to install PIL with \
'pip install PIL'")
    sys.exit(1)

# code copied from stackoverflow
# fixes cmd being a bitch about ansi colour codes
if os.name == 'nt':
    from ctypes import windll
    kernel = windll.kernel32
    kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)


# the starts of various error and warning messages
ERROR_MSG = "\x1b[38;5;196m[ERROR]:"
WARN_MSG = "\x1b[38;5;220m[WARNING]:"
INFO_MSG = "\x1b[38;5;27m[INFO]:"
INFO_IND = "\x1b[38;5;27m|___[INFO]:"
END_MSG = "\x1b[0m"


def main():
    """main function"""

    # one liner i found somewhere to get all the webp files
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk("./") for
             f in filenames if os.path.splitext(f)[1] == '.webp']

    num_format_len = max(len(str(len(files))), 1)
    file_format_len = min(max([len(file) for file in files]), 40)

    for file_num, file in enumerate(files):
        # progress string
        progress = f"\x1b[2K({file_num + 1:>{num_format_len}d}/{len(files)})"
        # more human readable filename string
        file_name = f"'{re.sub('^./', '', file)}'"

        # making sure files in the trash aren't included lest error spam
        # the leading quote and the os.path.split are to trim off garbage in
        # the recycle bin file path
        if "$RECYCLE.BIN" in file:
            print(f"{progress} {INFO_MSG} skipping \
'{os.path.split(file_name)[1]} - file is in the recycle bin\
{END_MSG}")
            continue

        # wrapped in a try block because every file operation
        # fucks up at some point
        try:
            print(f"{progress} converting {file_name}...", end="\r")

            image = Image.open(file)
            filename_new = file.replace(".webp", ".png")
            # more human readable new filename string
            file_new = f"'{re.sub('^./', '', filename_new)}'"

            # adding "_<number>" in order to
            # not overwrite other files
            filename_new = check_filename(filename_new)

            image.save(filename_new, "png")
            image.close()

            # removing webp
            os.remove(file)

            # clearing line and printing progress
            print(f"{progress} converted {file_name:<{file_format_len}}\
 -> {file_new}")

        except FileNotFoundError:
            print(f"{progress} {ERROR_MSG} {file_name} does not exist \
{END_MSG}")
        except FileExistsError:
            print(f"{progress} {WARN_MSG} {file_name} already exists\
{END_MSG}")
        # other errors
        except OSError as err:
            print(f"{progress} {ERROR_MSG} {file_name} not converted: {err}\
{END_MSG}")
    print("done.")


def check_filename(filename: str) -> str:
    """appends '_<number>' to the end of the filename
    if the file already exists
    note: this function only checks the directory it is run in.
    arguments:
        filename: str; file name
    returns:
        filename: str; file name but with _<number> on the end"""
    first_run_flag = True
    counter = 1
    while os.path.isfile(filename):
        counter += 1
        if first_run_flag:
            # padding allows for a different message if the same
            # filename is present several times
            print(f"{INFO_MSG} {filename} exists {END_MSG}")
            filename = re.sub(".png",
                              f" {counter}.png",
                              filename)
        else:
            # padding allows for a different message if the same
            # filename is present several times
            print(f"{INFO_IND} {filename} also exists {END_MSG}")
            filename = re.sub(" [0-9].png",
                              f" {counter}.png",
                              filename)
        first_run_flag = False

    return filename


if __name__ == "__main__":
    main()
    input("press enter to continue...")
