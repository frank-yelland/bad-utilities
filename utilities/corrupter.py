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
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
import random
import argparse
import errno


def corrupt_file(number_of_corruptions: int, file_path: str, **kwargs) -> None:
    """corrupt_file: corrupts file:
    args:
        number_of_corruptions: int; number of corruptions
        file_path: str; path to file to be corrupted
    kwargs:
        head: int; number of bytes in header to protect
        tail: int; number of bytes in tailer to protect
        verbose: bool; print progress info
    returns:
        None"""

    # optional header size
    head_size = 100
    tail_size = 0
    verbose = True

    if "head" in kwargs:
        head_size = kwargs["head"]
    if "tail" in kwargs:
        tail_size = kwargs["tail"]
    if "verbose" in kwargs:
        verbose = kwargs["verbose"]

    # butchering the filename so the file can have '_corrupted' stuck into it
    full_file_name = os.path.basename(file_path)
    file_name, file_extension = os.path.splitext(full_file_name)

    if verbose:
        print(f"reading {full_file_name}...", end="")

    # removing previous run
    try:
        os.remove(f"{file_name}_corrupted{file_extension}")
    except OSError:
        pass

    # reading content to array: with error handling for file read errors
    try:
        with open(file_path, "rb+") as file:
            file_content = file.read()
    except OSError as err:
        if err.errno == errno.EACCES:
            print(f"[ERROR]: {file_path}: access denied")
        elif err.errno == errno.EISDIR:
            print(f"[ERROR]: {file_path} is a directory")
        elif err.errno == errno.ENOENT:
            print(f"[ERROR]: {file_path} not found")
        else:
            print(f"[ERROR]: OSError: {err}: {file_path}")
        if verbose:
            print("done")
        return None

    # converting file from bytes (immutable) to list of ints (mutable)
    content = [byte for byte in file_content]

    if verbose:
        print(f"done\ncorrupting {full_file_name}...", end="")

    # flipping random bits
    size = os.path.getsize(file_path)
    for _ in range(number_of_corruptions):
        try:
            index = random.randint(head_size, size - 1 - tail_size)
        except ValueError:
            print("[ERROR]: head and tail protection overlap")
            exit(1)

        content[index] = content[index] ^ (1 << random.randint(0, 7))

    if verbose:
        print(f"done\nwriting {file_name}_corrupted{file_extension}...", end="")

    # writing array to file
    file_content = bytes(content)

    with open(f"{file_name}_corrupted{file_extension}", "wb+") as file:
        file.write(file_content)

    if verbose:
        print("done")


if __name__ == "__main__":
    size_dict = {
        "B": 1,
        "KB": 1000,
        "KiB": 1024,
        "MB": 1000000,
        "MiB": 1048576,
        "GB": 1000000000,
        "GiB": 1073741824
    }

    # the horrible line breaking is to appease flake8
    # the \b and \033[A are hacks to make the help option look correct
    parser = argparse.ArgumentParser(description="corrupts files: opens a set \
                                     of specified files, flips various bits at\
                                      random then saves them to\
                                      <filename>_corrupted.<extension>")
    parser.add_argument("-c", "--corruptions", action="store", type=int,
                        metavar="\b", default=100, help="\033[Anumber of\
                        flipped bit corruptions. increase to worsen the\
                        corruption")
    parser.add_argument("-d", "--head", action="store", type=int, metavar="\b",
                        default=100, help="number of heading bytes to protect,\
                        increase to protect more of a file's header")
    parser.add_argument("-t", "--tail", action="store", type=int, metavar="\b",
                        default=0, help="number of tailing bytes to protect.\
                        increase to protect trailing data")
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="prints progress indicators")
    parser.add_argument("-u", "--unit", choices=size_dict.keys(), metavar="\b",
                        default="B", help=f"select unit for header and tailer\
                        options. options: {', '.join(size_dict.keys())}")
    parser.add_argument('filepaths', nargs=argparse.REMAINDER,
                        help="paths to files to corrupt")

    args = parser.parse_args()

    try:
        multiplier = size_dict[args.unit]
    except KeyError:
        print(f"[ERROR]: invalid unit '{args.unit}'")
        exit(1)

    path_list = args.filepaths

    # asks for a file if none provided
    if path_list == []:
        print("[NOTE]: no paths specified")
        filepath = input("enter a file path> ")
        path_list.append(filepath)

    # corrupts all files in the list of files
    for filepath in path_list:
        corrupt_file(args.corruptions, filepath, head=(args.head * multiplier),
                     tail=(args.tail * multiplier), verbose=args.verbose)
