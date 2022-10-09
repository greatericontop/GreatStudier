"""Contains constants."""

#  Copyright (C) 2022-present greateric.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


VERSION = '1.2.0'


class C:
    bwhite = '\033[1;97m'
    no = '\033[9;91m'
    #
    white = '\033[0;97m'
    yellow = '\033[0;93m'
    green = '\033[0;92m'
    blue = '\033[0;94m'
    cyan = '\033[0;96m'
    red = '\033[0;91m'
    magenta = '\033[0;95m'
    black = '\033[0;90m'
    darkwhite = '\033[0;37m'
    darkyellow = '\033[0;33m'
    darkgreen = '\033[0;32m'
    darkblue = '\033[0;34m'
    darkcyan = '\033[0;36m'
    darkred = '\033[0;31m'
    darkmagenta = '\033[0;35m'
    darkblack = '\033[0;30m'
    end = '\033[0;0m'


SPACED_REPETITION = [
    -2147483648,  # default state (0); unstudied words go here
    14400,  # 4h (can review after first learning)
    86400,  # 1d
    259200,  # 3d
    604800,  # 7d
    1209600,  # 14d
    1814400,  # 21d
    2592000,  # 30d
    3888000,  # 45d
    5184000,  # 60d
    5184000,
    5184000,
    5184000,
    5184000,
    5184000,
    5184000,
    5184000,
    5184000,
    5184000,
    5184000,
    5184000,
    2147483647
]

NEW_CHUNK_SIZE = 8
REVIEW_CHUNK_SIZE = 15
AFTER_WRONG_RETURN_REP_TO = 1

CLEAR = '\n\n\n\n\n\n\n\n\n\n\n\n\033[H\033[2J'  # this ansi sequence *should* clear the screen
CONTINUE = f'{C.black}...{C.end}'
YES_DEFAULT_YES = {'y', '1', 'yes', 'true', 't', ''}
YES_DEFAULT_NO = {'y', '1', 'yes', 'true', 't'}

ILLEGAL_FILENAME_CHARS = [
    '/',
    '<',
    '>',
    ':',
    '"',
    '\\',
    '|',
    '?',
    '*',
    '&',
    '#',
    '{',
    '}',
    '=',
    '@',
    '`',
]

# Contains all accent transpositions for some languages. Some may be duplicated, but this is intentional.
ACCENT_TRANSPOSITION_TABLE = [
    # Spanish
    ('á', 'a'),
    ('é', 'e'),
    ('í', 'i'),
    ('ó', 'o'),
    ('ú', 'u'),
    ('ü', 'u'),
    ('ñ', 'n'),
    # French
    ('ç', 'c'),
    ('é', 'e'),
    ('â', 'a'),
    ('ê', 'e'),
    ('î', 'i'),
    ('ô', 'o'),
    ('û', 'u'),
    ('à', 'a'),
    ('è', 'e'),
    ('ù', 'u'),
    ('ë', 'e'),
    ('ï', 'i'),
    ('ü', 'u'),
    # German
    ('ß', 's'),
    ('ä', 'a'),
    ('ö', 'o'),
    ('ü', 'u'),
    # Chinese
    ('ā', 'a'),
    ('á', 'a'),
    ('ǎ', 'a'),
    ('à', 'a'),
    ('ē', 'e'),
    ('é', 'e'),
    ('ě', 'e'),
    ('è', 'e'),
    ('ī', 'i'),
    ('í', 'i'),
    ('ǐ', 'i'),
    ('ì', 'i'),
    ('ō', 'o'),
    ('ó', 'o'),
    ('ǒ', 'o'),
    ('ò', 'o'),
    ('ū', 'u'),
    ('ú', 'u'),
    ('ǔ', 'u'),
    ('ù', 'u'),
    ('ǖ', 'u'),
    ('ǘ', 'u'),
    ('ǚ', 'u'),
    ('ǜ', 'u'),
]
