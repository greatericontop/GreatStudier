"""Spanish Vocabulary Studying"""

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

import dataclasses
import enum
import time
import Levenshtein

import config
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


def validate_file(name: str) -> bool:
    with open(f'{config.get_set_directory()}{name}', 'r') as f:
        contents = f.readlines()[0]
    if contents.startswith('#gstudier'):
        return True
    else:
        return False


def load_words(name: str) -> list:
    with open(f'{config.get_set_directory()}{name}', 'r') as f:
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


def save_words(keys: list, out: str) -> None:
    with open(f'{config.get_set_directory()}{out}', 'w') as f:
        data = []
        for key in keys:
            data.append(f'{key.word}, {key.definition}, {key.last_covered}, {key.repetition_spot}')
        f.write('\n'.join(data))


def get_studyable(keys: list) -> tuple:
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


def validate(guess, answer) -> ValidationResult:
    guess = guess.lower()
    answer = answer.lower()
    if guess == answer:
        return ValidationResult.FULL_CORRECT
    lev_threshold = min(max(len(answer)//3, 1), 4)
    if Levenshtein.distance(guess, answer) <= lev_threshold:
        return ValidationResult.MOSTLY_CORRECT
    return ValidationResult.INCORRECT
