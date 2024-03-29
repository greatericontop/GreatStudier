"""Utilities"""

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
import pathlib as pl
import random
import string
import sys
import time
import rapidfuzz_damerau_levenshtein as lev

import config
from constants import *


class InvalidFileFormatError(RuntimeError):
    pass


@dataclasses.dataclass
class KeyData:
    word: str
    definition: str
    last_covered: int
    repetition_spot: int


class answer_mode(enum.Enum):
    TERM = 0
    DEFINITION = 1


def file_check(contents: list[str]) -> bool:
    return contents[0].lower().startswith('## * greatstudier *')


def load_words(name: str) -> list:
    path = pl.Path(config.get_set_directory()) / name
    if not path.exists():
        print(f'{C.red}The set file does not exist! Please choose a valid set.{C.end}\n'
              f'{C.red}Relaunch and try again to select a different set.{C.end}')
        config.config['set'] = None
        sys.exit(10)
    with path.open('r') as f:
        contents = f.read().split('\n')
    if not file_check(contents):
        raise InvalidFileFormatError(f'Expected first line "## * greatstudier *"; got "{contents[0].lower()}" instead')
    tokenized = []
    for line in contents:
        if len(line) == 0 or line.startswith('#'):
            continue
        data = [x.strip() for x in line.split('::')]
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


def save_words(keys: list, output_file_name: str) -> None:
    data = []
    for key in keys:
        if '::' in key.word or '::' in key.definition:
            print(f'{C.yellow}Your set contained some special characters used by GreatStudier, so we were forced to remove them. Sorry!{C.end}')
            key.word = key.word.replace('::', ' ')
            key.definition = key.definition.replace('::', ' ')
        data.append(f'{key.word} :: {key.definition} :: {key.last_covered} :: {key.repetition_spot}')
    data_to_dump = '\n'.join(data)
    save_data(f'## * greatstudier *\n{data_to_dump}', output_file_name)


def save_data(data: str, output_file_name: str) -> None:
    path = pl.Path(config.get_set_directory()) / output_file_name
    with path.open('w', encoding='utf-8') as f:
        f.write(data)


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


def validate(guess: str, answer: str) -> ValidationResult:
    guess = guess.lower().strip()
    answer = answer.lower().strip()
    if config.config['remove_language_accents']:
        for a, b in ACCENT_TRANSPOSITION_TABLE:
            guess = guess.replace(a, b)
            answer = answer.replace(a, b)
    if config.config['alpha_only']:
        for a in string.punctuation:
            guess = guess.replace(a, '')
            answer = answer.replace(a, '')
    if guess == answer:
        return ValidationResult.FULL_CORRECT
    mistakes_allowed = min(len(answer)//4, 4)  # 0..4 depending on the length of the answer
    if lev.distance(guess, answer) <= mistakes_allowed:
        return ValidationResult.MOSTLY_CORRECT
    return ValidationResult.INCORRECT


def probability_round(num: float) -> int:
    """Probability round float to the nearest integer."""
    int_part = int(num)
    frac_part = random.random() < (num - int_part)  # e.g., 40% for 0.4 to round to 1, otherwise 0
    return int_part + frac_part
