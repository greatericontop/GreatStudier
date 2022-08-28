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


VERSION = 'b1.3.0'


SPACED_REPETITION = [
    1,  # the default state that unstudied words can also go into
    60, 60,  # initial learnings
    14400,  # 4h
    86400,  # 1d
    259200,  # 3d
    604800,  # 7d
    1209600,  # 14d
    1814400,  # 21d
    2592000,  # 30d
    3888000,  # 45d
    5184000,  # 60d
    7776000,  # 90d
    7776000,
    7776000,
    7776000,
    7776000,
    2147483647
]
NEW_CHUNK_SIZE = 5
REVIEW_CHUNK_SIZE = 18
AFTER_WRONG_RETURN_REP_TO = 2
CLEAR = '\033[H\033[2J\033[3J'  # this ansi sequence *should* clear the screen

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
]
