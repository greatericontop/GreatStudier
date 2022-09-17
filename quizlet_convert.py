"""
Convert Quizlet sets into GreatStudier format.
Quizlet has an API, but it is nonexistent/broken, so we'll have to do some hacky things.
"""

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


import utils
from constants import *

LINE_SEPARATOR = ';;$;;'
ITEM_SEPARATOR = '==$=='


def convert_quizlet_set():
    prompt = ('In the Quizlet dashboard, select the EXPORT option.\n'
              f'Between the term and definition, choose CUSTOM and set it to {C.black}{ITEM_SEPARATOR}{C.end}.\n'
              f'Between rows, choose CUSTOM and set it to {C.black}{LINE_SEPARATOR}{C.end}.\n'
              'Copy the resulting text and enter it below.\n'
              '> ')
    quizlet_set = input(prompt)
    quizlet_items = quizlet_set.split(LINE_SEPARATOR)
    converted = []
    for quizlet_item in quizlet_items:
        if not quizlet_item:  # blank line with no text
            continue
        item = quizlet_item.split(ITEM_SEPARATOR)
        converted.append(utils.KeyData(item[0], item[1], -1, 0))
    target_location = input('Where would you like to save it? ')
    utils.save_words(converted, target_location)
    input(CONTINUE)
    print(CLEAR)
