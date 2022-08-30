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
import pathlib as pl


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
        with pl.Path('~/.greatstudier_config.py').expanduser().open('r') as f:
            return update_with_defaults(ast.literal_eval(f.read()))
    except FileNotFoundError:
        return update_with_defaults()


def save_config(data: dict) -> None:
    with pl.Path('~/.greatstudier_config.py').expanduser().open('w') as f:
        f.write(f'# Data for GreatStudier\n# Please do not touch this!\n\n{repr(data)}')


def get_set_directory() -> pl.Path:
    """Return the directory for the set (path is expanded) as a string."""
    if config['set_directory'] is None:
        return pl.Path('~/GreatStudier/').expanduser()
    return pl.Path(config['set_directory']).expanduser()


def create_set_directory_if_none() -> None:
    get_set_directory().mkdir(mode=0o700, exist_ok=True)


def reload_config() -> None:
    """Reload and fix any inconsistencies in the current config (call this when loading as well)."""
    create_set_directory_if_none()


config = load_config()
reload_config()
