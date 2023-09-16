#!/usr/bin/python3
"""
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

import argparse
import sys


def frequency_counter(file_path: str, **kwargs) -> dict:
    """frequency counter: counts frequency of ascii characters in text
    args:
        file_path: path to file
    kwargs:
        ignore: ignore capitalisation
        letters: only count letters
    returns:
        letter_dict: dict; dictionary of characters and their freqiencies in
                    frequency order"""

    ignore_capitalisation = kwargs.get("ignore", False)
    custom_charset = kwargs.get("charset", False)

    # creating the dictionary of characters
    letter_dict = {}

    if not custom_charset:
        for i in range(32, 127, 1):
            letter_dict.update({chr(i): 0})
    else:
        letter_dict = {key: 0 for key in custom_charset}

    # opening file with shitty error handling
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            content = file.read()
    except OSError as err:
        print(f"[ERROR]: {err}")
        exit(1)

    for character in content:
        # honestly can't think of a less scuffed way to do this
        # maybe capitalising the keys?
        if ignore_capitalisation:
            if character.upper() in letter_dict:
                letter_dict[character.upper()] += 1
            if character.lower() in letter_dict:
                letter_dict[character.lower()] += 1
        else:
            if character in letter_dict:
                letter_dict[character] += 1

    # sorting the dict to make the output more readable
    letter_dict = dict(sorted(letter_dict.items(), key=lambda x: x[1],
                       reverse=True))

    return letter_dict


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="prints out the frequency of\
                                     characters in text files")
    parser.add_argument("file_path",
                        type=str,
                        metavar="file path",
                        default="",
                        nargs="?",
                        help="path to file to analyse"
    )
    parser.add_argument("-r",
                        "--output-raw",
                        action="store_true",
                        default=False,
                        help="print unformatted"
    )
    parser.add_argument("-i",
                        "--ignore",
                        action="store_true",
                        default=False,
                        help="ignore capitalisation"
    )
    parser.add_argument("-c",
                        "--custom",
                        action="store",
                        default=False,
                        metavar="\b",
                        help="set custom character set; e.g.\
                        'ABCDEFGHIJKLMNOPQRSTUVWXYZ' for all capital letters"
    )

    args = parser.parse_args()

    file_path = args.file_path
    
    if file_path == "":
        for arg in sys.stdin:
            file_path = arg[:-1:]
            break
    if file_path == "" or file_path == None:
        print("[ERROR]: no file specified")
        exit(2)

    frequency = frequency_counter(file_path, ignore=args.ignore,
                                  charset=args.custom)

    if args.output_raw:
        print(frequency)
    else:
        print(f"frequencies in {args.file_path}")
        for key_value in frequency.items():
            key, value = key_value
            print(f"'{key}': {value}")

