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

import os
import random
import time
from typing import List

import config
import gamify
import quiz
import utils
from utils import C
from constants import *


def learn(words, new_terms) -> None:
    random.shuffle(new_terms)
    print(
        f'{CLEAR}You are ready to:\nLEARN x{C.darkcyan}{min(NEW_CHUNK_SIZE, len(new_terms))}{C.end}\n\nPress enter to continue.\n')
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
    utils.save_words(words, config.config['set'])


def review(words, review_terms) -> None:
    random.shuffle(review_terms)
    print(
        f'{CLEAR}You are ready to:\nREVIEW x{C.darkcyan}{min(REVIEW_CHUNK_SIZE, len(review_terms))}{C.end}\n\nPress enter to continue.\n')
    input()
    for i in range(min(REVIEW_CHUNK_SIZE, len(review_terms))):
        key = review_terms[i]
        quiz.quiz(key)
    print('You are done!')
    utils.save_words(words, config.config['set'])


def stats() -> None:
    data = gamify.gamify_data
    print(f"{C.green}You have {data['correct_answers']} correct answers.{C.end}")
    print(f"{C.red}You have {data['wrong_answers']} wrong answers.{C.end}")


def wipe_progress(words) -> None:
    # print(f'{C.red}Clearing ALL progress! Press enter to continue, only if you are sure.{C.end}')
    input()
    for key in words:
        key.last_covered = -1
        key.repetition_spot = 0
    utils.save_words(words, config.config['set'])


def choose_set() -> None:
    if not os.path.exists(config.get_set_directory()):
        config.create_set_directory()

    sets = os.listdir(config.get_set_directory())
    print_sets = "\n".join(sets)

    if len(sets) == 0:
        print(f'\n{C.cyan}You Currently Have No Sets Available, Import or Create New to continue.{C.end}')
    else:
        print(f'{C.cyan}Study Sets{C.end}\n{print_sets}\n')
        no_valid_set: bool = True
        while no_valid_set:
            word_set = input('Choose a set: ')
            if not word_set.endswith('.txt'):
                word_set += '.txt'
            if word_set in sets:
                config.config['set'] = word_set
                no_valid_set = False
            else:
                print('Invaild Set, Please choose a valid set.')


def open_options() -> None:
    options: str = f'Options\n'
    for i in config.config.keys():
        if i == 'set':
            continue
        options += f'{C.cyan}{i}{C.end}: {C.darkgreen}{config.config[i]}{C.end}\n'
    print(options)
    option_change = input('Please choose an option to change: ').lower()
    if option_change not in config.config.keys() or option_change == 'set':
        return print('That is not a vaild option.')
    if type(config.config[option_change]) is bool:
        config.config[option_change] = not config.config[option_change]
    else:
        new_option = input('What do you want to change it to (enter full path for set_directory): ')
        config.config[option_change] = new_option
    config.save_config(config.config)


def main():
    while config.config['set'] is None:
        cmd = input(
            'You have not chosen any sets to study.\n[C]hoose Set or Create [N]ew Set or [O]ptions or [E]xit: ').lower().strip()

        if cmd == 'e':
            return

        if cmd == 'c':
            choose_set()
        # elif cmd == 'n':
        #     new_set()
        elif cmd == 'o':
            open_options()
        else:
            print('That is not an option.')
            return

    study: bool = True

    while study:
        word_set = config.config['set']
        words = utils.load_words(word_set)
        print(f'Current set "{C.bwhite}{word_set}{C.end}"')
        new_terms, review_terms = utils.get_studyable(words)
        cmd = input(
            '[C]hoose Set or Create [N]ew Set or [O]ptions\n[L]earn or [R]eview or [S]tats or [E]xit: ').lower().strip()

        if cmd == 'e':
            study = False

        if cmd == 'l':
            learn(words, new_terms)
        elif cmd == 'r':
            review(words, review_terms)
        elif cmd == 's':
            stats()
        elif cmd == 'c':
            choose_set()
        # elif cmd == 'n':
        #     new_set()
        elif cmd == 'o':
            open_options()
        # elif cmd == '_wipe_progress':
        #     wipe_progress(words)
        else:
            print('That is not an option.')

        gamify.fix_level(print_stuff=True)
        if config.config['show_gamify']:
            gamify.show_level()
        gamify.save_gamify(gamify.gamify_data)
        config.save_config(config.config)
        wipe_progress(words)
        print(CLEAR)


if __name__ == '__main__':
    main()
