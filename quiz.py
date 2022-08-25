"""Quiz management."""

import time

import gamify
import utils
from utils import C
from constants import *


def quiz(key) -> bool:
    print(f'\n\nQUIZ: What is {C.cyan}{key.definition}{C.end}?')
    guess = input('>')
    result = utils.validate(guess, key.word)

    if result == utils.ValidationResult.FULL_CORRECT:
        print(f'{C.green}Correct!{C.end}')
        input()
        key.last_covered = int(time.time())
        key.repetition_spot += 1
        gamify.gamify_correct_answer(key.repetition_spot)
        return True

    elif result == utils.ValidationResult.MOSTLY_CORRECT:
        print(f'{C.darkgreen}Mostly correct! It actually was: {C.white}{key.word}{C.end}')
        if input() != '*':
            key.last_covered = int(time.time())
            key.repetition_spot += 1
            gamify.gamify_correct_answer(key.repetition_spot)
            return True
        else:
            print(f'{C.magenta}You have overwritten your answer to {C.red}WRONG{C.end}')
            key.repetition_spot = min(AFTER_WRONG_RETURN_REP_TO, key.repetition_spot)
            gamify.gamify_wrong_answer()
            return False

    else:
        print(f"{C.red}Sorry, that's incorrect! It actually was: {C.white}{key.word}{C.end}")
        if input() == '*':
            print(f'{C.magenta}You have overwritten your answer to {C.green}CORRECT{C.end}')
            key.last_covered = int(time.time())
            key.repetition_spot += 1
            gamify.gamify_correct_answer(key.repetition_spot)
            return True
        else:
            key.repetition_spot = min(AFTER_WRONG_RETURN_REP_TO, key.repetition_spot)
            gamify.gamify_wrong_answer()
            return False
