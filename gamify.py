"""Science! Fun! Gamification!"""

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

from utils import C


LEVEL_XP = 2000


def load_gamify() -> dict:
    """Load the gamify files."""
    try:
        with open(os.path.expanduser('~/.greatstudier_gamify.py'), 'r') as f:
            return ast.literal_eval(f.read())
    except FileNotFoundError:
        return {'level': 1, 'xp': 0, 'correct_answers': 0, 'wrong_answers': 0}


def save_gamify(data: dict) -> None:
    """Save the data provided to the gamify file."""
    with open(os.path.expanduser('~/.greatstudier_gamify.py'), 'w') as f:
        f.write(f'# Data for GreatStudier\n# Please do not touch this!\n\n{repr(data)}')


def fix_level(print_stuff: bool) -> None:
    """Increment the level if the XP is more than the threshold."""
    if gamify_data['xp'] >= LEVEL_XP:
        gamify_data['xp'] -= LEVEL_XP
        gamify_data['level'] += 1
        if print_stuff:
            print(f"{C.white}---------- {C.blue}You're now level {C.darkcyan}{gamify_data['level']}{C.blue}! {C.white}----------{C.end}")


def show_level() -> None:
    """Print out the level."""
    print(f"{C.white}---------- {C.green}You're currently level {dashboard()}. {C.white}----------{C.end}")


def prestige() -> str:
    """Return the prestige (with color)."""
    level = gamify_data['level']
    if level >= 100:
        l1, l2, l3 = str(level)
        return f'{C.red}[{C.yellow}{l1}{C.green}{l2}{C.darkcyan}{l3}{C.blue}✶{C.darkmagenta}]{C.end}'
    if level >= 90:
        l1, l2 = str(level)
        return f'{C.cyan}[{C.darkcyan}{l1}{C.blue}{l2}{C.darkblue}✶{C.darkmagenta}]{C.end}'
    if level >= 80:
        return f'{C.darkred}[{C.red}{level}{C.darkyellow}✶{C.yellow}]{C.end}'
    if level >= 70:
        return f'{C.cyan}[{level}✶]{C.end}'
    if level >= 60:
        return f'{C.magenta}[{level}✶]{C.end}'
    if level >= 50:
        return f'{C.darkred}[{level}✶]{C.end}'
    if level >= 40:
        return f'{C.blue}[{level}✶]{C.end}'
    if level >= 30:
        return f'{C.darkgreen}[{level}✶]{C.end}'
    if level >= 20:
        return f'{C.darkyellow}[{level}✶]{C.end}'
    if level >= 10:
        return f'{C.bwhite}[{level}✶]{C.end}'
    return f'{C.darkwhite}[{level}✶]{C.end}'


def dashboard() -> str:
    """Return the level and progress."""
    xp = gamify_data['xp']
    return f'{prestige()} {C.black}({xp}/{LEVEL_XP}){C.end}'


def gamify_correct_answer(level: int = 0) -> None:
    """Register a correct answer."""
    gamify_data['correct_answers'] += 1
    gamify_data['xp'] += 20 + 10*level


def gamify_wrong_answer() -> None:
    """Register a wrong."""
    gamify_data['wrong_answers'] += 1
    gamify_data['xp'] += 1


gamify_data = load_gamify()
