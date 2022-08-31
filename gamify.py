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
import math
import pathlib as pl

from utils import C


LEVEL_XP = 20000


def load_gamify() -> dict:
    """Load the gamify files."""
    try:
        with pl.Path('~/.greatstudier_gamify.py').expanduser().open('r') as f:
            return ast.literal_eval(f.read())
    except FileNotFoundError:
        return {'level': 1, 'xp': 0, 'correct_answers': 0, 'wrong_answers': 0}


def save_gamify(data: dict) -> None:
    """Save the data provided to the gamify file."""
    with pl.Path('~/.greatstudier_gamify.py').expanduser().open('w') as f:
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
        star = '❂'
        l1, l2, l3 = str(level)
        return f'{C.red}[{C.yellow}{l1}{C.green}{l2}{C.darkcyan}{l3}{C.blue}{star}{C.darkmagenta}]{C.end}'
    if level >= 90:
        star = '✦'
        l1, l2 = str(level)
        return f'{C.cyan}[{C.darkcyan}{l1}{C.blue}{l2}{C.darkblue}{star}{C.darkmagenta}]{C.end}'
    if level >= 80:
        star = '✪'
        return f'{C.darkred}[{C.red}{level}{C.darkyellow}{star}{C.yellow}]{C.end}'
    if level >= 70:
        star = '✸'
        return f'{C.cyan}[{level}{star}]{C.end}'
    if level >= 60:
        star = '✭'
        return f'{C.magenta}[{level}{star}]{C.end}'
    if level >= 50:
        star = '✵'
        return f'{C.darkred}[{level}{star}]{C.end}'
    if level >= 40:
        star = '✶'
        return f'{C.blue}[{level}{star}]{C.end}'
    if level >= 30:
        star = '✰'
        return f'{C.darkgreen}[{level}{star}]{C.end}'
    if level >= 20:
        star = '✬'
        return f'{C.darkyellow}[{level}{star}]{C.end}'
    if level >= 10:
        star = '★'
        return f'{C.bwhite}[{level}{star}]{C.end}'
    star = '⭑'
    return f'{C.darkwhite}[{level}{star}]{C.end}'


def dashboard() -> str:
    """Return the level and progress."""
    xp = gamify_data['xp']
    return f'{prestige()} {C.black}({xp}/{LEVEL_XP}){C.end}'


def gamify_correct_answer(level: int = 0) -> None:
    """Register a correct answer."""
    gamify_data['correct_answers'] += 1
    gamify_data['xp'] += 30 + 10*level


def gamify_wrong_answer() -> None:
    """Register a wrong."""
    gamify_data['wrong_answers'] += 1
    gamify_data['xp'] += 1


def get_skill() -> int:
    """Return the 'skill score'"""
    correct = gamify_data['correct_answers']  # "positive rating"
    wrong = gamify_data['wrong_answers']  # "negative rating"
    n = correct + wrong
    if n == 0:
        return 0
    # Wilson Lower Bound
    p_hat = 1.0 * correct / n
    Z = 2.652  # z_alpha/2, alpha=0.004, 99.6% (yes this is overdone) right-tailed confidence
    radicand = (p_hat*(1-p_hat) + Z*Z/(4*n)) / n
    top = p_hat + (Z*Z)/(2*n) - Z*math.sqrt(radicand)
    bottom = 1 + Z*Z/n
    return int(3200 * (top / bottom))


gamify_data = load_gamify()
