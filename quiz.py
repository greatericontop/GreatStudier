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

import time

import gamify
import utils
from utils import C
from constants import *


def quiz(key, extra: str = '', overwrite_knowledge_level: int = None) -> bool:
    if overwrite_knowledge_level is None:
        overwrite_knowledge_level = key.repetition_spot + 1
    print(f'\n\n{extra}QUIZ: What is {C.cyan}{key.definition}{C.end}?')
    guess = input(f'{C.darkblue}>{C.end} ')
    result = utils.validate(guess, key.word)

    if result == utils.ValidationResult.FULL_CORRECT:
        print(f'{C.green}Correct!{C.end}')
        input()
        key.last_covered = int(time.time())
        key.repetition_spot += 1
        gamify.gamify_correct_answer(overwrite_knowledge_level)
        return True

    elif result == utils.ValidationResult.MOSTLY_CORRECT:
        print(f'{C.darkgreen}Mostly correct! It actually was: {C.white}{key.word}{C.end}')
        if input() != '*':
            key.last_covered = int(time.time())
            key.repetition_spot += 1
            gamify.gamify_correct_answer(overwrite_knowledge_level)
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
            key.last_covered = int(time.time())
            key.repetition_spot += 1
            gamify.gamify_correct_answer(overwrite_knowledge_level)
            return True
        else:
            key.repetition_spot = min(AFTER_WRONG_RETURN_REP_TO, key.repetition_spot)
            gamify.gamify_wrong_answer()
            return False
