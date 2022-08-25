"""Spanish Vocabulary Studying"""

import dataclasses
import enum
import time
import Levenshtein

from constants import *


class C:
    bwhite = '\033[1;97m'
    white = '\033[0;97m'
    yellow = '\033[0;93m'
    green = '\033[0;92m'
    blue = '\033[0;94m'
    cyan = '\033[0;96m'
    red = '\033[0;91m'
    magenta = '\033[0;95m'
    black = '\033[0;90m'
    darkwhite = '\033[0;37m'
    darkyellow = '\033[0;33m'
    darkgreen = '\033[0;32m'
    darkblue = '\033[0;34m'
    darkcyan = '\033[0;36m'
    darkred = '\033[0;31m'
    darkmagenta = '\033[0;35m'
    darkblack = '\033[0;30m'
    end = '\033[0;0m'


@dataclasses.dataclass
class KeyData:
    word: str
    definition: str
    last_covered: int
    repetition_spot: int


def load_words(name: str):
    with open(name, 'r') as f:
        contents = f.read().split('\n')
    tokenized = []
    for line in contents:
        if len(line) == 0 or line.startswith('#'):
            continue
        data = [x.strip() for x in line.split(',')]
        # data[0]: Key
        # data[1]: Definition
        # data[2]: Last covered
        # data[3]: Repetition spot
        assert len(data) == 4
        tokenized.append(KeyData(
            word=data[0].strip(),
            definition=data[1].strip(),
            last_covered=int(data[2]),
            repetition_spot=int(data[3])
        ))
    return tokenized


def save_words(keys: list, out: str):
    with open(out, 'w') as f:
        data = []
        for key in keys:
            data.append(f'{key.word}, {key.definition}, {key.last_covered}, {key.repetition_spot}')
        f.write('\n'.join(data))


def get_studyable(keys: list):
    new = []
    review = []
    for key in keys:
        if key.last_covered + SPACED_REPETITION[key.repetition_spot] <= time.time():
            if key.repetition_spot == 0:
                new.append(key)
            else:
                review.append(key)
    return new, review


class ValidationResult(enum.Enum):
    FULL_CORRECT = 0
    MOSTLY_CORRECT = 1
    INCORRECT = 2


def validate(guess, answer):
    guess = guess.lower()
    answer = answer.lower()
    if guess == answer:
        return ValidationResult.FULL_CORRECT
    lev_threshold = min(max(len(answer)//3, 1), 4)
    if Levenshtein.distance(guess, answer) <= lev_threshold:
        return ValidationResult.MOSTLY_CORRECT
    return ValidationResult.INCORRECT
