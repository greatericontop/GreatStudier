"""GreatStudier"""

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

import random
import time

import gamify
import quiz
import utils
from utils import C
from constants import *


def learn(words, new_terms) -> None:
    random.shuffle(new_terms)
    print(f'{CLEAR}You are ready to:\nLEARN x{C.darkcyan}{min(NEW_CHUNK_SIZE, len(new_terms))}{C.end}\n\nPress enter to continue.\n')
    input()
    study_indices = list(range(min(NEW_CHUNK_SIZE, len(new_terms))))
    for i in study_indices:
        key = new_terms[i]
        print(f'\n\n{C.yellow}{key.word} {C.green}= {C.darkyellow}{key.definition}{C.end}')
        while True:
            if input().lower() == key.word.lower():
                break
    print(f'{CLEAR}Ready for the quiz?')
    input()
    quiz_number = 0
    while study_indices:
        quiz_number += 1
        if quiz_number != 1:
            print(f'{CLEAR}Sorry, you got some wrong. Try those again! (Quiz #{quiz_number})\n')
        random.shuffle(study_indices)
        for i in study_indices.copy():
            key = new_terms[i]
            if quiz.quiz(key):
                study_indices.remove(i)
    print('You are done!')
    utils.save_words(words, 'words.txt')


def review(words, review_terms) -> None:
    random.shuffle(review_terms)
    print(f'{CLEAR}You are ready to:\nREVIEW x{C.darkcyan}{min(REVIEW_CHUNK_SIZE, len(review_terms))}{C.end}\n\nPress enter to continue.\n')
    input()
    for i in range(min(REVIEW_CHUNK_SIZE, len(review_terms))):
        key = review_terms[i]
        quiz.quiz(key)
    print('You are done!')
    utils.save_words(words, 'words.txt')


def stats() -> None:
    data = gamify.gamify_data
    print(f"{C.green}You have {data['correct_answers']} correct answers.{C.end}")
    print(f"{C.red}You have {data['wrong_answers']} wrong answers.{C.end}")


def wipe_progress(words) -> None:
    print(f'{C.red}Clearing ALL progress! Press enter to continue, only if you are sure.{C.end}')
    input()
    for key in words:
        key.last_covered = -1
        key.repetition_spot = 0
    utils.save_words(words, 'words.txt')


def main():
    words = utils.load_words('words.txt')
    new_terms, review_terms = utils.get_studyable(words)
    cmd = input('[L]earn or [R]eview or [S]tats: ').lower().strip()

    if cmd == 'l':
        learn(words, new_terms)
    elif cmd == 'r':
        review(words, review_terms)
    elif cmd == 's':
        stats()
    elif cmd == '_wipe_progress':
        wipe_progress(words)
    else:
        print('That is not an option.')
        return

    gamify.fix_level(print_stuff=True)
    gamify.show_level()
    gamify.save_gamify(gamify.gamify_data)


if __name__ == '__main__':
    main()
