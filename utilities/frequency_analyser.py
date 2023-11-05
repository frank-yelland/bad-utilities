#!/usr/bin/python3

"""frequency analyser tool

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

from copy import deepcopy
import argparse
import sys
import re
import itertools
import json
import math
import common

ideal_frequency = {
    'E': 0.1259063863781522,
    'T': 0.10006782449472729,
    'A': 0.07925578930508564,
    'O': 0.07528914392832355,
    'I': 0.07378434974501549,
    'N': 0.06892787863567965,
    'S': 0.06096690441491981,
    'R': 0.05995843525133622,
    'H': 0.05484885815584606,
    'L': 0.03803115181020215,
    'D': 0.03686844618630578,
    'U': 0.03051311306521236,
    'C': 0.02966085775245839,
    'M': 0.02456512239058604,
    'W': 0.021092824643031576,
    'F': 0.021057231613728626,
    'G': 0.02053717790780219,
    'Y': 0.019817407759675866,
    'P': 0.01863097344957753,
    'B': 0.015449352107997161,
    'V': 0.011067454722700642,
    'K': 0.009040629442949318,
    'X': 0.0018271088375514369,
    'J': 0.0013525351135121027,
    'Q': 0.0008878483420569212,
    'Z': 0.0005951945455659984
}

# ideal_frequency = {
#     'E': 0.12702,
#     'T': 0.09056,
#     'A': 0.08167,
#     'O': 0.07507,
#     'I': 0.06966,
#     'N': 0.06749,
#     'S': 0.06327,
#     'H': 0.06094,
#     'R': 0.05987,
#     'D': 0.04253,
#     'L': 0.04025,
#     'C': 0.02782,
#     'U': 0.02758,
#     'M': 0.02406,
#     'W': 0.0236,
#     'F': 0.02228,
#     'G': 0.02015,
#     'Y': 0.01974,
#     'P': 0.01929,
#     'K': 0.01772,
#     'B': 0.01492,
#     'V': 0.00978,
#     'J': 0.00253,
#     'X': 0.0025,
#     'Q': 0.00095,
#     'Z': 0.00074
# }


def generate_tetragram_dict(alphabet: str =
                            "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> dict:
    """generates a tetragram dict
    optional arguments:
        alphabet: set of characters (not including lowercase or punctuation)
                  that make up the tetragrams
    returns:
        tet_dict: dict of tetragrams"""
    tet_dict: dict = {}
    alphabet = "".join(set(alphabet)).upper()

    alphabet = re.sub(r"[^a-zA-Z\d\s]|[0-9]", "", alphabet)
    for tetragram in itertools.product(alphabet, repeat=4):
        key = "".join(tetragram)
        tet_dict.update({key: 0})

    return tet_dict


def get_file_content(f_path: str) -> str:
    """gets content of file and does some basic processing on it
    arguments:
        f_path: str; path to file
    returns:
        file_content: str; file content
    """

    # opening file with shitty error handling
    try:
        with open(f_path, "r", encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        common.print_error(f"file '{f_path}' not found")
        sys.exit(1)
    except IsADirectoryError:
        common.print_error(f"file '{f_path}' is a directory")
        sys.exit(1)
    except OSError as err:
        common.print_error(f"os error; {err}")
        sys.exit(1)

    return content


def frequency_counter(string: str, **kwargs) -> dict:
    """frequency counter: counts frequency of ascii characters in text
    args:
        f_path: path to file
    kwargs:
        ignore: bool; ignore capitalisation
        custom_charset: str; set of characters to count
        tgram: bool; whether to search for tetragrams
    returns:
        letter_dict: dict; dictionary of characters and their freqiencies in
                    frequency order"""

    ignore_capitalisation: bool = kwargs.get("ignore", False)
    custom_charset = kwargs.get("charset", False)
    tetragram: bool = kwargs.get("tgram", False)
    word: bool = kwargs.get("word", False)

    n: int = 4 if tetragram and not word else 1

    # creating the dictionary of characters
    letter_dict: dict = {}

    if not custom_charset:
        # 1st is all characters (we will only be using capital letters)
        # for i in range(32, 127, 1):
        if ignore_capitalisation:
            for i in range(65, 91, 1):
                letter_dict.update({chr(i): 0})
        else:
            for i in range(32, 127, 1):
                letter_dict.update({chr(i): 0})

    else:
        letter_dict = {key: 0 for key in custom_charset.split(",")}

    if tetragram:
        letter_dict = generate_tetragram_dict(alphabet=letter_dict.keys())

    if word:
        letter_dict = {}
        # removing non-alphabetic characters
        string = re.sub(r"[^a-zA-Z\d\s]", "", string)
        # first one doesn't catch newlines for some reason
        string = re.sub("\n", "", string)
        # removing double spaces
        string = re.sub("  ", " ", string)
        string = string.split(" ")

    for index, character in enumerate(string):
        character = string[index:index+n]
        # honestly can't think of a less scuffed way to do this
        # maybe capitalising the keys?
        character = "".join(character)
        if ignore_capitalisation:
            if character.upper() in letter_dict:
                letter_dict[character.upper()] += 1
            elif word:
                letter_dict.update({character.upper(): 1})
        else:
            if character in letter_dict:
                letter_dict[character] += 1
            elif word and len(character) <= 45:
                letter_dict.update({character: 1})

    # sorting the dict to make the output more readable
    letter_dict = dict(sorted(letter_dict.items(), key=lambda x: x[1],
                       reverse=True))

    return letter_dict


def determine_correlation(std_letter_dict: dict) -> float:
    """determines if there is significant correlation with the
    distribution of characters in english and the given text sample
    globals:
        ideal_frequency: dict; dict containting the portion
                            of the english language taken up by
                            the letter of the key
    arguments:
        std_letter_dict: dict; keys as capital latin letters &
                         non-normalised values
    returns:
        correlation: float | None; correlation derived from how close the
                     line of best fit is to 1"""

    # checking the keys match
    if std_letter_dict.keys() != ideal_frequency.keys():
        return None

    # normalising dict values to sum to 1
    normalised_dict = normalise(std_letter_dict)

    # calculating r value
    # the code is fucked because the pmcc is horrible

    x_list = list(normalised_dict.values())
    y_list = list(ideal_frequency.values())

    sum_x: float = sum(x_list)
    sum_y: float = sum(y_list)

    sum_x_y: float = 0.0
    for index in range(26):
        sum_x_y += x_list[index] * y_list[index]

    # Sxx = Σ(x²) - Σ(x)²/n
    s_xx: float = sum([i ** 2 for i in x_list]) - ((sum_x ** 2) / 26)
    # Syy = Σ(y²) - Σ(y)²/n
    # s_yy = sum([i ** 2 for i in y_list]) - ((sum_y ** 2) / 26)

    # Sxy = Σ(xy) - Σ(x)Σ(y)/n
    s_xy: float = sum_x_y - ((sum_x * sum_y) / 26)

    #      Sxy
    # b = -----
    #      Sxx
    b_mult: float = s_xy / s_xx

    # a = ȳ - b * x̄
    # a_mult = (sum_y / len(y_list)) - (b_add * (sum_x / len(x_list)))

    # a function that peaks at y = 1

    correlation: float = 1 / ((10 * (b_mult ** 2)) - (20 * b_mult) + 11)

    return correlation


def automatic_key_map(freq_dict: dict) -> dict:
    """automatically maps frequent letters to frequent letters in english
    globals:
        ideal_frequency: dict; dict containting the portion
                            of the english language taken up by
                            the letter of the key
    arguments:
        freq_dict: dict; dict with the uppercase alphabet as the keys and
                   frequencies as the values
    returns:
        mapped: dict; dict with the keys as the most common letters in the text
                and values as the corresponding most common english letters
        """
    # checking the keys match
    if freq_dict.keys() != ideal_frequency.keys():
        return None

    # more convenient to have as a list
    letter_list = list(ideal_frequency.keys())

    mapped: dict = deepcopy(freq_dict)

    for index, letter in enumerate(mapped):
        mapped[letter] = letter_list[index]

    # sorts dict alphabetically
    mapped = dict(sorted(mapped.items()))

    return mapped


def save_dict(sample_dict: dict, filename: str = "frequencies.json") -> None:
    """saves dict to json file"""
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(sample_dict, json_file, indent=4)


def normalise(freq_dict: dict) -> dict:
    """normalises a dict so that the sum of the values are equal to 1
    arguments:
        freq_dict: dict; dict to normalise
    returns
        norm_dict: dict; normalised dict"""
    value_sum: int = sum(freq_dict.values())

    if value_sum == 0:
        common.print_error("cannot normalise dict (division by 0)")
        sys.exit(1)

    norm_dict: dict = deepcopy(freq_dict)

    for i in norm_dict:
        norm_dict[i] = norm_dict[i] / value_sum

    return norm_dict


def take_log(freq_dict: dict, base: int = 10) -> dict:
    """takes the log base a dict so that the sum of the values are equal to 1
    arguments:
        freq_dict: dict; dict to normalise
    optional arguments:
        base: int; default 10; t
    returns
        log_dict: dict; logbased dict"""
    log_dict = deepcopy(freq_dict)

    for key, value in log_dict.items():
        if value == 0:
            log_dict[key] = -1
        else:
            log_dict[key] = math.log(value, base)

    return log_dict


def print_dict(sample_dict: dict, **kwargs) -> None:
    """prints the dict prettily
    arguments:
        sample_dict: dict; dict to print
    keyword arguments
        strip: bool; strip zeros or not"""
    max_key_len = min(max([len(key) for key in sample_dict.keys()]) + 2, 12)
    quote: str = "'"
    strip = kwargs.get("strip", False)
    for key_value in sample_dict.items():
        key, value = key_value
        if strip and value == 0:
            continue
        print(f"{quote + key + quote:>{max_key_len}}: {value}")


def main():
    """main function"""
    parser = argparse.ArgumentParser(description="prints out the frequency of\
                                     characters in a given passage. default\
                                     character set is uppercase latin letters")
    parser.add_argument("file_path",
                        type=str,
                        metavar="file path",
                        default="",
                        nargs="?",
                        help="path to file to analyse"
                        )
    parser.add_argument("-i",
                        "--ignore",
                        action="store_true",
                        default=False,
                        help="if enabled, do not ignore capitalisation"
                        )
    parser.add_argument("-c",
                        "--custom",
                        action="store",
                        default=False,
                        metavar=" ",
                        help="set custom character set; e.g. \
'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z' for all lowercase \
letters"
                        )
    parser.add_argument("-m",
                        "--auto-map",
                        action="store_true",
                        default=False,
                        help="automatically map the letter frequency as a\
 substitution cipher key. does not work with tetragram or word options active"
                        )
    parser.add_argument("-p",
                        "--correlation",
                        action="store_true",
                        default=False,
                        help="finds correlation between character frequency\
 in the text and the character frequency of english"
                        )
    parser.add_argument("-v",
                        "--normalise",
                        action="store_true",
                        default=False,
                        help="normalise the frequency so that the sum of the\
 frequency values is 1"
                        )
    parser.add_argument("-b",
                        "--log-base",
                        action="store",
                        type=int,
                        default=None,
                        metavar=" ",
                        help="takes the logbase value of the frequency"
                        )
    parser.add_argument("-t",
                        "--tetragram",
                        action="store_true",
                        default=False,
                        help="look for 4-long sets of letters of a given size \
instead of individual characters. will only ever count capital letters and \
spaces"
                        )
    parser.add_argument("-w",
                        "--word",
                        action="store_true",
                        default=False,
                        help="look for word frequencies instead of letter \
frequencies. overrides tetragram. words are alphabetic only"
                        )
    parser.add_argument("-n",
                        "--nth-letter",
                        action="store",
                        type=int,
                        default=1,
                        metavar=" ",
                        help="analyses only every nth letter. \
have a number and 1 (ie 3,1) to search every nth (3rd) letter (alternatively\
 use just 3 to ignore the other 2 numbers)"
                        )
    parser.add_argument("-o",
                        "--strip-zeros",
                        action="store_true",
                        default=False,
                        help="don't print frequencies equal to 0"
                        )
    parser.add_argument("-s",
                        "--save",
                        action="store",
                        default=None,
                        metavar=" ",
                        help="store raw dict (only the frequency) in a file"
                        )
    parser.add_argument("-l",
                        "--length",
                        action="store_true",
                        default=False,
                        help="count length of sample (number of counterd \
letters, words, tetragrams)"
                        )
    parser.add_argument("-u",
                        "--upper",
                        action="store_true",
                        default=False,
                        help="capitalise input texts"
                        )
    parser.add_argument("-a",
                        "--alphabetical",
                        action="store_true",
                        default=False,
                        help="remove spaces and punctuatuion from input texts"
                        )

    args = parser.parse_args()

    letter_sets = args.nth_letter

    if letter_sets is not None:
        try:
            if isinstance(letter_sets, int):
                letter_sets = [letter_sets]
            else:
                letter_sets = tuple([int(i) for i in letter_sets.split(",")])
        except (TypeError, ValueError):
            common.print_error("invalid number pair for the nth letter \
argument")
    else:
        letter_sets = [1]

    # =====- gleaning file path from input -=====

    file_path = args.file_path

    if file_path == "":
        for arg in sys.stdin:
            file_path = arg[:-1:]
            break

    if file_path is None:
        common.print_error("no file specified")
        sys.exit(2)

    content = get_file_content(file_path)
    if args.upper:
        content = content.upper()
    if args.alphabetical:
        content = re.sub("[^a-zA-Z ]", "", content)

    content_list = []
    n = letter_sets[0]

    if len(letter_sets) > 1:
        if letter_sets[1] != 0 and letter_sets[1] is not None:
            for i in range(n):
                content_list.append(content[i::n])
    else:
        content_list.append(content[::n])

    print(f"frequencies in {args.file_path}:")

    for index, content_string in enumerate(content_list):
        if len(content_list) > 1:
            print(f"\nsection {index+1}/{len(content_list)}:")

        # ======- running the frequency tests -======

        frequency = frequency_counter(content_string,
                                      ignore=(not args.ignore),
                                      charset=args.custom,
                                      tgram=args.tetragram,
                                      word=args.word
                                      )

        r_value = determine_correlation(frequency)

        # ========- various post-processing -========

        # normalises the frequency
        if args.normalise:
            print_frequency = normalise(frequency)
        elif args.log_base:
            print_frequency = take_log(frequency)
        else:
            print_frequency = frequency

        filename: str = args.save

        if args.save:
            if index > 1:
                if filename.endswith(".json"):
                    filename = filename.replace(".json", f"_{index}.json")
                else:
                    filename += f"_{index}.json"
            else:
                if not filename.endswith(".json"):
                    filename += ".json"
            if args.strip_zeros:
                print_frequency = {key: item for key, item in
                                   print_frequency.items() if item != 0}
            save_dict(print_frequency, filename)
        else:
            print_dict(print_frequency, strip=args.strip_zeros)

        if args.length:
            print(sum(print_frequency.values()))

        # printing pmcc compared to normal english
        if args.correlation:
            print(f"correlation value is: {r_value}")

        # automatic mapping of the frequencies to english
        if args.auto_map and not (args.tetragram or args.word):
            auto_map = automatic_key_map(frequency)
            print("auto mapping:")
            print_dict(auto_map)
            print(f"mapping as key:\n{''.join(auto_map.values())}")


if __name__ == "__main__":
    main()
