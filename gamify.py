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
import datetime as dt

from constants import C


def level_xp(level: int) -> int:
    """Return required amount to go from the current level to the next."""
    return {
        1: 1500,
        2: 6000,
        3: 12500,
    }.get(level, 20000)  # default 20k


def load_gamify() -> dict:
    """Load the gamify files."""
    try:
        with pl.Path('~/.greatstudier_gamify.py').expanduser().open('r') as f:
            data = ast.literal_eval(f.read())
        # automatically migrate outdated file
        if 'quests' not in data:
            NEVER_RESET = '2000-01-01'
            data['quests'] = {
                # daily quests: if 'last_reset' is yesterday and 'completed' is True, reset it
                # weekly quests: if 'last_reset' is not today and today is FRIDAY and 'completed' is True
                # after resetting, set 'last_reset' to the current day and 'completed' to False
                'login_bonus': {'last_reset': NEVER_RESET, 'completed': False},
                'study_50': {'last_reset': NEVER_RESET, 'completed': False, 'progress': 0},
                'answer_correct_500': {'last_reset': NEVER_RESET, 'completed': False, 'progress': 0},
                'review_100': {'last_reset': NEVER_RESET, 'completed': False, 'progress': 0},
            }
        return data
    except FileNotFoundError:
        return {'level': 1, 'xp': 0, 'correct_answers': 0, 'wrong_answers': 0}


def save_gamify(data: dict) -> None:
    """Save the data provided to the gamify file."""
    with pl.Path('~/.greatstudier_gamify.py').expanduser().open('w') as f:
        f.write(f'# Data for GreatStudier\n# Please do not touch this!\n\n{repr(data)}')


def fix_level(print_stuff: bool) -> None:
    """Increment the level if the XP is more than the threshold."""
    if gamify_data['xp'] >= level_xp(gamify_data['level']):
        gamify_data['xp'] -= level_xp(gamify_data['level'])
        gamify_data['level'] += 1
        if print_stuff:
            print(f'---------- LEVEL UP! ----------')
            print(f"{C.bwhite}---------- {C.blue}You're now level {C.darkcyan}{gamify_data['level']}{C.blue}! {C.bwhite}----------{C.end}")


def show_level() -> None:
    """Print out the level."""
    print(f"{C.bwhite}---------- {C.green}You're currently level {dashboard()}. {C.bwhite}----------{C.end}")


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
    total = level_xp(gamify_data['level'])
    return f'{prestige()} {C.black}({xp}/{total}){C.end}'


def gamify_correct_answer(level: int = 0) -> None:
    """Register a correct answer."""
    gamify_data['correct_answers'] += 1
    gamify_data['xp'] += 10*level
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
    p = top / bottom
    return int(1500*p**4 + 700*p**3 + 400*p**2 + 500*p + 100)


def update_quests() -> None:
    """Update completed daily and weekly quests."""
    today = dt.date.today()
    quests = gamify_data['quests']
    # TODO: try to not repeat yourself & move boilerplate into a method to reduce clutter
    # daily
    if dt.date.fromisoformat(quests['login_bonus']['last_reset']) != today and quests['login_bonus']['completed']:
        quests['login_bonus']['last_reset'] = today
        quests['login_bonus']['completed'] = False
    if dt.date.fromisoformat(quests['study_50']['last_reset']) != today and quests['study_50']['completed']:
        quests['study_50']['last_reset'] = today
        quests['study_50']['completed'] = False
        quests['study_50']['progress'] = 0
    # weekly (only resets on Monday, weekday #4)
    if today.weekday() == 0:
        if dt.date.fromisoformat(quests['study_100']['last_reset']) != today and quests['study_100']['completed']:
            quests['study_100']['last_reset'] = today
            quests['study_100']['completed'] = False
            quests['study_100']['progress'] = 0
        if dt.date.fromisoformat(quests['review_100']['last_reset']) != today and quests['review_100']['completed']:
            quests['review_100']['last_reset'] = today
            quests['review_100']['completed'] = False
            quests['review_100']['progress'] = 0


def print_quests() -> None:
    """Print the current quests."""
    # login_bonus
    print(f'Daily Quest: {C.cyan}Study Today{C.end}\n'
          f'Complete a study session.\n'
          f'+50 XP\n')
    print('COMPLETED' if gamify_data['quests']['login_bonus']['completed'] else 'INCOMPLETE')
    # study_50
    print(f'\nDaily Quest: {C.cyan}Great Studier{C.end}\n'
          f'Study 50 cards.\n'
          f'+100 XP\n')
    print('COMPLETED' if gamify_data['quests']['study_50']['completed']
          else f"{gamify_data['quests']['study_50']['progress']}/50")
    # answer_correct_500
    print(f'\nWeekly Quest: {C.cyan}Question Solver Co{C.end}\n'
          f'Answer 500 questions correctly.'
          f'+1500 XP\n')
    print('COMPLETED' if gamify_data['quests']['answer_correct_500']['completed']
          else f"{gamify_data['quests']['answer_correct_500']['progress']}/500")
    # review_100
    print(f'\nWeekly Quest: {C.cyan}Memorization Master{C.end}\n'
          f'Successfully review 100 cards.\n'
          f'+1500 XP\n')
    print('COMPLETED' if gamify_data['quests']['review_100']['completed']
          else f"{gamify_data['quests']['review_100']['progress']}/100")


# TODO: also refactor this because it's boilerplate as well, like a :_incr_progress: method
# TODO: maybe even turn login_bonus into completing 2 study sessions
#       instead of 1 to make it harder and to be consistent with the other quests
def complete_login_bonus():
    """Complete the login bonus if you're able to."""
    quest = gamify_data['quests']['login_bonus']
    if not quest['completed']:
        quest['completed'] = True
        gamify_data['xp'] += 50
        print(f'{C.green}----------------------------------------{C.end}\n'
              f'{C.green}You have completed Study Today! (+50 XP){C.end}\n'
              f'{C.green}----------------------------------------{C.end}')
def increment_study():
    """Increment the study 50 quest if you're able to."""
    quest = gamify_data['quests']['study_50']
    if not quest['completed']:
        quest['progress'] += 1
        if quest['progress'] >= 50:
            quest['completed'] = True
            gamify_data['xp'] += 100
            print(f'{C.green}-------------------------------------------{C.end}\n'
                  f'{C.green}You have completed Great Studier! (+100 XP){C.end}\n'
                  f'{C.green}-------------------------------------------{C.end}')
def increment_answer_correct():
    """Increment the answer 500 correctly quest if you're able to."""
    quest = gamify_data['quests']['answer_correct_500']
    if not quest['completed']:
        quest['progress'] += 1
        if quest['progress'] >= 500:
            quest['completed'] = True
            gamify_data['xp'] += 1500
            print(f'{C.green}-------------------------------------------------{C.end}\n'
                  f'{C.green}You have completed Question Solver Co! (+1500 XP){C.end}\n'
                  f'{C.green}-------------------------------------------------{C.end}')
def increment_review_correct():
    """Increment the review 100 correctly quest if you're able to."""
    quest = gamify_data['quests']['review_100']
    if not quest['completed']:
        quest['progress'] += 1
        if quest['progress'] >= 100:
            quest['completed'] = True
            gamify_data['xp'] += 1500
            print(f'{C.green}--------------------------------------------------{C.end}\n'
                  f'{C.green}You have completed Memorization Master! (+1500 XP){C.end}\n'
                  f'{C.green}--------------------------------------------------{C.end}')


gamify_data = load_gamify()
