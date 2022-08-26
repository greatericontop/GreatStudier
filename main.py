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

import config
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
    utils.save_words(words, config.config['set'])


def review(words, review_terms) -> None:
    random.shuffle(review_terms)
    print(f'{CLEAR}You are ready to:\nREVIEW x{C.darkcyan}{min(REVIEW_CHUNK_SIZE, len(review_terms))}{C.end}\n\nPress enter to continue.\n')
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
    print(f"{C.green}You're currently level {gamify.prestige()}")


def wipe_progress(words) -> None:
    print(f'{C.red}Clearing ALL progress! Press enter to continue, only if you are sure.{C.end}')
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
        print(f'\n{C.yellow}You currently have no sets available. Import or create a new set to continue.{C.end}')
    else:
        print(f'{C.cyan}Study Sets{C.end}\n{print_sets}\n')
        no_valid_set: bool = True
        while no_valid_set:
            word_set = input('Choose a set: ')
            if word_set == '':
                return
            if not word_set.endswith('.txt'):
                word_set += '.txt'
            if word_set in sets:
                config.config['set'] = word_set
                no_valid_set = False
            else:
                print(f'{C.red}Invalid Set! Please choose a valid set.{C.end}')
    config.save_config(config.config)


def open_options() -> None:
    options = 'Options\n'
    for i in config.config.keys():
        if i == 'set':
            continue
        options += f'{C.cyan}{i}{C.end}: {C.darkgreen}{config.config[i]}{C.end}\n'
    print(options)
    option_change = input('Please choose an option to change: ').lower()
    if option_change == '':
        return
    if option_change not in config.config.keys() or option_change == 'set':
        return print('That is not a valid option.')
    if type(config.config[option_change]) is bool:
        config.config[option_change] = not config.config[option_change]
    else:
        new_option = input('What do you want to change it to (enter full path for set_directory): ')
        config.config[option_change] = new_option
    config.save_config(config.config)


# def new_set() -> None:


def main():
    print(f'{C.green}GreatSudier Version {VERSION}{C.end}')

    while True:
        if config.config['set'] is None:
            learning_available = False
            prompt = (f'{C.red}It seems you do not have a set chosen!{C.end}\n'
                      '[C]hoose Set\n'
                      '[N]ew Set\n'
                      '[O]ptions\n'
                      '[S]tats\n'
                      '[Q]uit\n'
                      f'{C.darkblue}>{C.end} ')
        else:
            learning_available = True
            prompt = ('[L]earn\n'
                      '[R]eview\n'
                      '[W]ipe Progress\n'
                      '[C]hoose Set\n'
                      '[N]ew Set\n'
                      '[O]ptions\n'
                      '[S]tats\n'
                      '[Q]uit\n'
                      f'{C.darkblue}>{C.end} ')
            word_set = config.config['set']
            words = utils.load_words(word_set)
            print(f'Current set "{C.bwhite}{word_set}{C.end}"')
            new_terms, review_terms = utils.get_studyable(words)
        cmd = input(prompt).lower().strip()

        if cmd in {'quit', 'q'}:
            break
        # begin learning available
        if cmd in {'learn', 'l'} and learning_available:
            learn(words, new_terms)
        elif cmd in {'review', 'r'} and learning_available:
            review(words, review_terms)
        elif cmd in {'_wipe_progress', 'w'} and learning_available:
            wipe_progress(words)
        # end learning available
        elif cmd in {'choose', 'c'}:
            choose_set()
        elif cmd in {'new', 'n'}:
            print('[Sorry, this is unavailable at the moment.]')
        elif cmd in {'options', 'o'}:
            open_options()
        elif cmd in {'stats', 's'}:
            stats()
        else:
            print('That is not an option.')

    gamify.fix_level(print_stuff=True)
    if config.config['show_gamify']:
        gamify.show_level()
    # SAVE STUFF
    gamify.save_gamify(gamify.gamify_data)
    config.save_config(config.config)


if __name__ == '__main__':
    main()
