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
import time

import utils
from constants import C, MAX_TIME_PER_QUESTION, SECONDS_PER_XP


CURRENT_GAMIFY_REVISION = 1


def level_xp(level: int) -> int:
    """Return required amount to go from the current level to the next."""
    return {
        0: 250,
        1: 500,
        2: 1000,
        3: 1750,
    }.get(level % 100, 2500)


def load_gamify() -> dict:
    """Load the gamify files."""
    try:
        with pl.Path('~/.greatstudier_gamify.py').expanduser().open('r') as f:
            data = ast.literal_eval(f.read())
        # automatically migrate outdated file
        if 'rev' not in data:
            data['rev'] = CURRENT_GAMIFY_REVISION
        # add study timers
        if 'total_time_studied' not in data:
            data['total_time_studied'] = 0  # Note: this is stored in CENTISECONDS
        # merge in un-added quests
        NEVER_RESET = '2000-01-01'
        bare_quests = {
            'login_bonus': {'last_reset': NEVER_RESET, 'completed': False, 'progress': 0},
            'study_50': {'last_reset': NEVER_RESET, 'completed': False, 'progress': 0},
            'answer_correct_500': {'last_reset': NEVER_RESET, 'completed': False, 'progress': 0},
            'review_100': {'last_reset': NEVER_RESET, 'completed': False, 'progress': 0},
            'study_hours': {'last_reset': NEVER_RESET, 'completed': False, 'progress': 0},
        }
        bare_quests.update(data.get('quests', {}))
        data['quests'] = bare_quests
        return data
    except FileNotFoundError:
        return {'level': 1, 'xp': 0, 'correct_answers': 0, 'wrong_answers': 0, 'rev': CURRENT_GAMIFY_REVISION}


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
    if level >= 1000:
        star = '❂'
        l1, l2, l3, l4 = str(level)
        return (f'{C.red}['
                f'{C.darkyellow}{l1}'
                f'{C.yellow}{l2}'
                f'{C.green}{l3}'
                f'{C.darkcyan}{l4}'
                f'{C.blue}{star}'
                f'{C.darkmagenta}]'
                f'{C.end}')
    if level >= 900:
        star = '✦'
        return f'{C.cyan}[{C.blue}{level}{C.darkblue}{star}{C.darkmagenta}]{C.end}'
    if level >= 800:
        star = '✸'
        return f'{C.darkred}[{C.red}{level}{C.darkyellow}{star}{C.yellow}]{C.end}'
    if level >= 700:
        star = '✪'
        return f'{C.cyan}[{level}{star}]{C.end}'
    if level >= 600:
        star = '✭'
        return f'{C.magenta}[{level}{star}]{C.end}'
    if level >= 500:
        star = '✵'
        return f'{C.darkred}[{level}{star}]{C.end}'
    if level >= 400:
        star = '✶'
        return f'{C.blue}[{level}{star}]{C.end}'
    if level >= 300:
        star = '✰'
        return f'{C.darkgreen}[{level}{star}]{C.end}'
    if level >= 200:
        star = '✬'
        return f'{C.darkyellow}[{level}{star}]{C.end}'
    if level >= 100:
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
    return int(500*p**16 + 500*p**8 + 700*p**6 + 400*p**5 + 400*p**4 + 200*p**3 + 400*p**2 + 100)


def _update_quest(quest, today: dt.date) -> None:
    """(Helper) Update a single quest."""
    # 'last_reset' is set immediately after completing
    # then, the next day/week, this gets called, and it resets it
    # (if it's called again on the same day it won't reset again)
    if dt.date.fromisoformat(quest['last_reset']) != today and quest['completed']:
        quest['last_reset'] = today.isoformat()
        quest['completed'] = False
        quest['progress'] = 0
def update_quests() -> None:
    """Update completed daily and weekly quests."""
    today = dt.date.today()  # current date in local time
    quests = gamify_data['quests']
    # daily
    _update_quest(quests['login_bonus'], today)
    _update_quest(quests['study_50'], today)
    # weekly (only resets on Monday, weekday #4)
    # you'll have to complete it the day before for this to reset you
    if today.weekday() == 0:
        _update_quest(quests['answer_correct_500'], today)
        _update_quest(quests['review_100'], today)
        _update_quest(quests['study_hours'], today)


def print_quest_progress() -> None:
    """Print the current quest progress."""
    # header
    print(f'\n{C.yellow}QUESTS{C.end}')
    # login_bonus
    print(f'Daily Quest: {C.cyan}Study Today{C.end}: Complete a study session. ({C.cyan}+100{C.end})')
    print(f'{C.green}COMPLETED{C.end}' if gamify_data['quests']['login_bonus']['completed']
          else f"{C.cyan}{gamify_data['quests']['login_bonus']['progress']}{C.end}/1")
    # study_50
    print(f'Daily Quest: {C.cyan}Great Studier{C.end}: Study 50 cards. ({C.cyan}+150{C.end})')
    print(f'{C.green}COMPLETED{C.end}' if gamify_data['quests']['study_50']['completed']
          else f"{C.cyan}{gamify_data['quests']['study_50']['progress']}{C.end}/50")
    # answer_correct_500
    print(f'Weekly Quest: {C.cyan}Question Solver Co{C.end}: Answer 500 questions correctly. ({C.cyan}+2000{C.end})')
    print(f'{C.green}COMPLETED{C.end}' if gamify_data['quests']['answer_correct_500']['completed']
          else f"{C.cyan}{gamify_data['quests']['answer_correct_500']['progress']}{C.end}/500")
    # review_100
    print(f'Weekly Quest: {C.cyan}Memorization Master{C.end}: Successfully review 100 cards. ({C.cyan}+2000{C.end})')
    print(f'{C.green}COMPLETED{C.end}' if gamify_data['quests']['review_100']['completed']
          else f"{C.cyan}{gamify_data['quests']['review_100']['progress']}{C.end}/100")
    # study_hours
    print(f'Weekly Quest: {C.cyan}Study Buddy{C.end}: Study for 1 hour. ({C.cyan}+1500{C.end})')
    seconds = gamify_data['quests']['study_hours']['progress'] // 100
    print(f'{C.green}COMPLETED{C.end}' if gamify_data['quests']['study_hours']['completed']
          else f"{C.cyan}{seconds // 60:02}:{seconds % 60:02}{C.end}/60:00")


def _increment_progress(quest_id: str, human_name: str,
                        required_amount: int, given_xp: int,
                        *, amount: int = 1
                        ) -> None:
    """(Helper) Increment the progress of a quest."""
    quest = gamify_data['quests'][quest_id]
    if not quest['completed']:
        quest['progress'] += amount
        if quest['progress'] >= required_amount:
            quest['completed'] = True
            quest['last_reset'] = dt.date.today().isoformat()
            gamify_data['xp'] += given_xp
            print(f'\n\n\n'
                  f'{C.green}------------------------------------------------------------{C.end}\n'
                  f'{C.green}You have completed {human_name}! (+{given_xp} XP){C.end}\n'
                  f'{C.green}------------------------------------------------------------{C.end}\n'
                  f'\n\n')
def increment_login_bonus() -> None:
    _increment_progress('login_bonus', 'Study Today', 1, given_xp=100)
def increment_study() -> None:
    _increment_progress('study_50', 'Great Studier', 50, given_xp=150)
def increment_answer_correct() -> None:
    _increment_progress('answer_correct_500', 'Question Solver Co', 500, given_xp=2000)
def increment_review_correct() -> None:
    _increment_progress('review_100', 'Memorization Master', 100, given_xp=2000)
def increment_study_hours(centiseconds: int) -> None:
    _increment_progress('study_hours', 'Study Buddy', 3600_00, given_xp=1500, amount=centiseconds)


# Timers: run :start_study_clock(): and :end_study_clock():.
# The globals here feel wrong, but there's no point in adding classes here.

start_time: float = None


def start_study_clock() -> None:
    """Start the study clock."""
    global start_time
    if start_time is not None:
        raise RuntimeError("Can't start study clock while one is running")
    start_time = time.perf_counter()


def end_study_clock() -> None:
    """End the study clock."""
    global start_time
    if start_time is None:
        raise RuntimeError("Can't end study clock while it is not running")
    end_time = time.perf_counter()
    total_time = min(end_time - start_time, MAX_TIME_PER_QUESTION)
    centiseconds = int(total_time * 100)
    increment_study_hours(centiseconds)
    gamify_data['total_time_studied'] += centiseconds
    gamify_data['xp'] += utils.probability_round(total_time / SECONDS_PER_XP)
    start_time = None


def dashboard_time_studied() -> str:
    """Get the time studied in a human-readable format."""
    study_time = gamify_data['total_time_studied'] // 100
    hours = study_time // 3600
    minutes = (study_time // 60) % 60
    seconds = study_time % 60
    return f'{hours}h {minutes}m {seconds}s'


gamify_data = load_gamify()
