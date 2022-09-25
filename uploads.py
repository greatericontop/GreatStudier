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


class FailedRequestError(RuntimeError):
    """Custom exception to raise when failing a request."""


def safely_request(func: callable, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except requests.exceptions.ConnectionError as e:
        raise FailedRequestError('Failed to connect. Check your internet connection and try again.') from e
    except requests.exceptions.RequestException as e:
        raise FailedRequestError(f'Failed to make request for some other reason. Details: {e}') from e


def encode_set(data: list[KeyData]) -> str:
    """Encode the set data into a string to be uploaded later."""
    text = []
    for key in data:
        text.append(f'{key.word} :: {key.definition} :: -1 :: 0')
    return '## * greatstudier * upload *\n' + '\n'.join(text)


def _paste_make_file(name: str, content: str) -> dict:
    """Make a paste.gg API file object with given name and content (as a string encoded in utf-8)."""
    return {
        'name': name,
        'content': {
            'format': 'text',
            'highlight_language': 'python',
            'value': content
        }
    }


def find_set(target_name: str) -> str:
    """Find the set and return its ID if it exists, otherwise return None. Requires a key."""
    username = config.config['paste_username']
    headers = {'Authorization': f"Key {config.config['paste_api_key']}"}
    resp = safely_request(requests.get, f'https://api.paste.gg/v1/users/{username}',
                          headers=headers)
    for paste in resp.json()['result']:
        if paste['name'] == target_name: # TODO: can this be combined with :edit_set:?
            return paste['id']
    return None


def edit_set(data: list[KeyData], paste_id: str) -> None:
    """Instead of uploading, edit an already existing paste.gg paste. Requires a key."""
    text = encode_set(data)
    headers = {'Authorization': f"Key {config.config['paste_api_key']}"}
    # get the file id
    resp = safely_request(requests.get, f'https://api.paste.gg/v1/pastes/{paste_id}',
                          headers=headers)
    main_file_id = resp.json()['result']['files'][0]['id']
    new_file = _paste_make_file('__', text)
    del new_file['name']
    # patch the specified file
    resp = safely_request(requests.patch, f'https://api.paste.gg/v1/pastes/{paste_id}/files/{main_file_id}',
                          json=new_file,
                          headers=headers)
    if resp.status_code != 204:
        print(resp.json())
        raise requests.exceptions.ConnectionError(f'status code {resp.status_code} is not 200')


def upload_set(data: list[KeyData], name: str) -> tuple[str, str]:
    """Upload the given data and name to paste.gg, and return a tuple of the url to it and key to delete it."""
    text = encode_set(data)
    headers = {'Content-Type': 'application/json'}
    if config.config['paste_api_key'] is not None:
        headers['Authorization'] = f"Key {config.config['paste_api_key']}"
    resp = safely_request(requests.post, 'https://api.paste.gg/v1/pastes',
                          json={
                             'name': name,
                             'description': f'Set {name} for GreatStudier',
                             'visibility': 'unlisted',
                             'files': [
                                 _paste_make_file(name, text),
                             ]
                         },
                          headers=headers)
    # check for errors
    if resp.json()['status'] == 'error':
        raise FailedRequestError(f"API error! {resp.json()['error']}")
    # get data
    result = resp.json()['result']
    if 'deletion_key' in result:
        how_to_delete = f"deletion key {result['deletion_key']}"
    else:
        how_to_delete = 'delete using account'
    return f"https://paste.gg/{result['id']}", how_to_delete


def _download_set(paste_id: str) -> tuple[str, str]:
    """Return the data inside the set. Return a tuple of the data and paste's name."""
    resp = safely_request(requests.get, f'https://api.paste.gg/v1/pastes/{paste_id}',
                          params={'full': 'true'})
    if resp.json()['status'] == 'error':
        print(resp.json())
        raise FailedRequestError(f"API error! {resp.json()['error']}")
    try:
        text = resp.json()['result']['files'][0]['content']['value']
        name = resp.json()['result']['name']
    except (KeyError, IndexError):
        raise FailedRequestError('Unexpected response! Check that the paste is in the proper format and try again.')
    return text, name


def download_set(link: str) -> tuple[str, str]:
    """Actually download it from a link."""
    if 'paste.gg' in link:  # assume it's a full link if it has the `paste.gg` in it
        actual_id = link.split('/')[-1]
    else:
        actual_id = link
    return _download_set(actual_id)
