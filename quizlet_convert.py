"""
Convert Quizlet sets into GreatStudier format.
Quizlet has an API, but it is nonexistent/broken, so we'll have to do some hacky things.
"""
import traceback

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

import requests

import utils
import uploads
from constants import *

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    pass

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'}


def get_quizlet_set(link: str) -> list:
    """Returns the set from quizlet"""
    converted = []
    try:
        soup = BeautifulSoup(requests.get(link, headers=HEADERS).content, 'html.parser')
    except NameError as e:
        print(f'{C.yellow}========================================{C.end}\n'
              f'{C.red}BeautifulSoup is not installed.{C.end}\n'
              f'{C.red}You can still use the rest of GreatStudier, but you must{C.end}\n'
              f'{C.red} install BeautifulSoup in order to use this feature.{C.end}\n'
              f'{C.yellow}========================================{C.end}')
        raise uploads.FailedRequestError(e)
    try:
        data = soup.find('div', 'SetPageTerms-termsList').find_all('div', 'SetPageTerms-term')
    except AttributeError as e:
        print(f'{C.black}Error info:\n{traceback.format_exc()}\n')
        raise uploads.FailedRequestError('Make sure that the quizlet set is not private.')
    for terms in data:
        term = terms.find_all('span')
        converted.append(utils.KeyData(term[0].text, term[1].text, -1, 0))
    return converted


def convert_quizlet_set() -> None:
    print(CLEAR)
    quizlet_set = input('Enter a Quizlet link to convert: ')
    if 'https://quizlet.com/' not in quizlet_set or not quizlet_set:
        print(f'{C.red}Invalid Quizlet Link! Please include the "https://quizlet.com/".{C.end}')
        input(CONTINUE)
        print(CLEAR)
        return
    try:
        converted = get_quizlet_set(quizlet_set)
    except uploads.FailedRequestError as e:
        print(f'{C.red}Failed to download set! {e}{C.end}')
        input(CONTINUE)
        print(CLEAR)
        return
    target_location = input('Where would you like to save it? ')
    if not target_location:
        print(f'{C.red}Nothing was provided!{C.end}')
        input(CONTINUE)
        print(CLEAR)
        return
    utils.save_words(converted, target_location)
    print(f'{C.green}Set downloaded successfully.{C.end}')
    input(CONTINUE)
    print(CLEAR)
