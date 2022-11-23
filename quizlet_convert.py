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

from bs4 import BeautifulSoup

import requests

import utils
import uploads
from constants import *

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'}


def get_quizlet_set(link: str) -> list:
    """Returns the set from quizlet"""
    converted = []
    soup = BeautifulSoup(requests.get(link, headers=HEADERS).content, 'html.parser')
    try:
        data = soup.find('section', "SetPage-termsList").find_all('div', 'SetPageTerms-term')
    except AttributeError:
        raise uploads.FailedRequestError('Make sure that the quizlet set is not private.')
    for terms in data:
        term = terms.find_all('span')
        converted.append(utils.KeyData(term[0].text, term[1].text, -1, 0))
    return converted


def convert_quizlet_set() -> None:
    print(CLEAR)
    quizlet_set = input('Enter a Quizlet link to convert: ')
    if 'quizlet.com' not in quizlet_set:
        print(f'{C.red}Invalid Quizlet Link!{C.end}')
        input(CONTINUE)
        print(CLEAR)
        return
    target_location = input('Where would you like to save it? ')
    try:
        converted = get_quizlet_set(quizlet_set)
    except uploads.FailedRequestError as e:
        print(f'{C.red}Failed to download set! {e}{C.end}')
        input(CONTINUE)
        print(CLEAR)
        return
    utils.save_words(converted, target_location)
    print(f'{C.green}Set downloaded successfully.{C.end}')
    input(CONTINUE)
    print(CLEAR)
