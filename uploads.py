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

import config

if TYPE_CHECKING:
    from utils import KeyData


def upload_set(data: list[KeyData], name: str) -> tuple[str, str]:
    """Upload the given data and name to paste.gg, and return a tuple of the url to it and key to delete it."""
    text = []
    for key in data:
        text.append(f'{key.word} :: {key.definition} :: -1 :: 0')
    text = '## * greatstudier * upload *\n' + '\n'.join(text)
    headers = {'Content-Type': 'application/json'}
    if config.config['paste_api_key'] is not None:
        headers['Authorization'] = f"Key {config.config['paste_api_key']}"
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
                         headers=headers)
    if resp.json()['status'] == 'error':
        return f"ERROR: {resp.json()['error']}", 'ERROR'
    result = resp.json()['result']
    if 'deletion_key' in result:
        how_to_delete = f"deletion key {result['deletion_key']}"
    else:
        how_to_delete = 'delete using account'
    return f"https://paste.gg/{result['id']}", how_to_delete


def _download_set(paste_id: str) -> tuple[str, str]:
    """Return the data inside the set. Return a tuple of the data and paste's name."""
    resp = requests.get(f'https://api.paste.gg/v1/pastes/{paste_id}',
                        params={'full': 'true'})
    if resp.json()['status'] == 'error':
        print(resp.json())
        raise RuntimeError(f"Response returned error! {resp.json()['error']}")
    try:
        text = resp.json()['result']['files'][0]['content']['value']
        name = resp.json()['result']['name']
    except (KeyError, IndexError):
        raise RuntimeError('Unable to find the data from the response!')  # to be caught later
    return text, name


def download_set(link: str) -> tuple[str, str]:
    """Actually download it from a link."""
    if 'paste.gg' in link:  # assume it's a full link if it has the `paste.gg` in it
        actual_id = link.split('/')[-1]
    else:
        actual_id = link
    return _download_set(actual_id)
