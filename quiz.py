"""Quiz management."""

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

import time
from typing import TYPE_CHECKING

import gamify
import utils
from constants import *

if TYPE_CHECKING:
    from utils import KeyData


def correct_answer_increment_knowledge(key: KeyData):
    key.last_covered = int(time.time())
    key.repetition_spot += 1
    gamify.gamify_correct_answer(key.repetition_spot)
    gamify.increment_answer_correct()


def correct_answer_study(key: KeyData):
    """Don't affect spaced repetition."""
    gamify.gamify_correct_answer(1)
    gamify.increment_answer_correct()


def quiz(key: KeyData, extra: str = '', increment_knowledge_level: bool = True) -> bool:
    on_correct = correct_answer_increment_knowledge if increment_knowledge_level else correct_answer_study
    print(f'\n\n{extra}QUIZ: What is {C.cyan}{key.definition}{C.end}?')
    guess = input(f'{C.darkblue}>{C.end} ')
    result = utils.validate(guess.strip(), key.word.strip())
    gamify.increment_study()

    if result == utils.ValidationResult.FULL_CORRECT:
        print(f'{C.green}Correct!{C.end}')
        input()
        on_correct(key)
        return True

    elif result == utils.ValidationResult.MOSTLY_CORRECT:
        print(f'{C.darkgreen}Mostly correct! It actually was: {C.white}{key.word}{C.end}')
        if input() != '*':
            on_correct(key)
            return True
        else:
            print(f'You have overwritten your answer to {C.red}WRONG{C.end}')
            key.repetition_spot = min(AFTER_WRONG_RETURN_REP_TO, key.repetition_spot)
            gamify.gamify_wrong_answer()
            return False

    else:
        print(f"{C.red}Sorry, that's incorrect! It actually was: {C.white}{key.word}{C.end}")
        if input() == '*':
            print(f'You have overwritten your answer to {C.green}CORRECT{C.end}')
            on_correct(key)
            return True
        else:
            key.repetition_spot = min(AFTER_WRONG_RETURN_REP_TO, key.repetition_spot)
            gamify.gamify_wrong_answer()
            return False
