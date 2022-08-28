"""GreatStudier configuration manager"""

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

import ast
import os


def update_with_defaults(original_config: dict = None) -> dict:
    """Update a config dict IN PLACE with default values, and return it as well."""
    if original_config is None:
        original_config = {}
    # add default values if they don't already exist
    if 'set' not in original_config:
        original_config['set'] = None
    if 'set_directory' not in original_config:
        original_config['set_directory'] = None
    if 'show_gamify' not in original_config:
        original_config['show_gamify'] = True
    if 'paste_api_key' not in original_config:
        original_config['paste_api_key'] = None
    return original_config


def load_config() -> dict:
    try:
        with open(os.path.expanduser('~/.greatstudier_config.py'), 'r') as f:
            return update_with_defaults(ast.literal_eval(f.read()))
    except FileNotFoundError:
        return update_with_defaults()


def save_config(data: dict) -> None:
    with open(os.path.expanduser('~/.greatstudier_config.py'), 'w') as f:
        f.write(f'# Data for GreatStudier\n# Please do not touch this!\n\n{repr(data)}')


def get_set_directory() -> str:
    """Return the directory for the set (path is expanded) as a string."""
    if config['set_directory'] is None:
        return os.path.expanduser('~/GreatStudier/')
    return os.path.expanduser(config['set_directory'])


def create_set_directory() -> None:
    os.mkdir(get_set_directory())


config = load_config()
