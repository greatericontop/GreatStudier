"""Upload manager."""

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

from __future__ import annotations

import requests
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils import KeyData


# TODO: allow you to use an api key
def upload_set(data: list[KeyData], name: str) -> tuple[str, str]:
    """Upload the given data and name to paste.gg, and return a tuple of the url to it and key to delete it."""
    text = []
    for key in data:
        text.append(f'{key.word}, {key.definition}, -1, 0')
    text = '## * greatstudier * upload *\n' + '\n'.join(text)
    resp = requests.post('https://api.paste.gg/v1/pastes',
                         json={
                             'name': name,
                             'description': f'Set {name} for GreatStudier',
                             'visibility': 'unlisted',
                             'files': [
                                 {
                                     'name': name,
                                     'content': {
                                         'format': 'text',
                                         'highlight_language': 'python',
                                         'value': text
                                     }
                                 }
                             ]
                         },
                         headers={'Content-Type': 'application/json'})
    if resp.json()['status'] == 'error':
        return 'ERROR', 'ERROR'
    result = resp.json()['result']
    return f"https://paste.gg/p/anonymous/{result['id']}", result['deletion_key']
