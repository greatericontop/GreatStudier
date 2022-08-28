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


def load_config() -> dict:
    try:
        with open(os.path.expanduser('~/.greatstudier_config.py'), 'r') as f:
            return ast.literal_eval(f.read())
    except FileNotFoundError:
        return {'set': None, 'set_directory': None, 'show_gamify': True}


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
