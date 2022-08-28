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
import signal
import sys

import config
import gamify
import motd
import quiz
import uploads
import utils
from utils import C
from constants import *


def terminate_handler(sig, frame):
    print(f'{C.red}Caught Control-C, exiting.')
    gamify.save_gamify(gamify.gamify_data)
    config.save_config(config.config)
    sys.exit(0)


signal.signal(signal.SIGINT, terminate_handler)


def learn(words, new_terms) -> None:
    random.shuffle(new_terms)
    print(f'{CLEAR}You are ready to:\nLEARN x{C.darkcyan}{min(NEW_CHUNK_SIZE, len(new_terms))}{C.end}\n')
    study_indices = list(range(min(NEW_CHUNK_SIZE, len(new_terms))))
    for i in study_indices:
        key = new_terms[i]
        print(f'\n\n{C.yellow}{key.word} {C.green}= {C.darkyellow}{key.definition}{C.end}')
        while True:
            if input().lower() == key.word.lower():
                break
    print(f'{CLEAR}Ready for the quiz?')
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
    print(f'{CLEAR}You are ready to:\nREVIEW x{C.darkcyan}{min(REVIEW_CHUNK_SIZE, len(review_terms))}{C.end}\n')
    for i in range(min(REVIEW_CHUNK_SIZE, len(review_terms))):
        key = review_terms[i]
        quiz.quiz(key)
    print('You are done!')
    utils.save_words(words, config.config['set'])


def stats() -> None:
    data = gamify.gamify_data
    print(f'{CLEAR}{C.green}Statistics{C.end}')
    print(f"{C.green}You have {data['correct_answers']} correct answers.{C.end}")
    print(f"{C.red}You have {data['wrong_answers']} wrong answers.{C.end}")
    if data['wrong_answers'] != 0:
        print(f"Correctness ratio: {data['correct_answers'] / data['wrong_answers']:.2f}")
    print(f"{C.green}You're currently level {gamify.prestige()}\n\n")


def wipe_progress(words) -> None:
    print(f'{C.red}Clearing ALL progress for this set! Continue only if you are sure.{C.end}')
    input()
    for key in words:
        key.last_covered = -1
        key.repetition_spot = 0
    utils.save_words(words, config.config['set'])
    print(CLEAR)


def choose_set() -> None:
    if not os.path.exists(config.get_set_directory()):
        config.create_set_directory()

    sets = os.listdir(config.get_set_directory())
    print_sets = '\n'.join(sets)

    if len(sets) == 0:
        print(f'\n{C.yellow}You currently have no sets available. Import or create a new set to continue.{C.end}')
    else:
        print(f'{CLEAR}{C.cyan}Available Study Sets{C.end}\n{print_sets}\n{C.darkgreen}Press [Enter] to exit.{C.end}\n')
        while True:
            word_set = input('Choose a set: ')
            if not word_set:
                break
            if word_set in sets:
                config.config['set'] = word_set
                break
            else:
                print(f'{C.red}Invalid Set! Please choose a valid set.{C.end}')
    config.save_config(config.config)
    print(CLEAR)


def open_settings() -> None:
    settings = 'Options\n'
    for i in config.config.keys():
        if i == 'set':
            continue
        settings += f'{C.cyan}{i}{C.end}: {C.darkgreen}{config.config[i]}{C.end}\n'
    print(settings)
    print(f'{C.darkgreen}Press [Enter] to exit.{C.end}')
    settings_change = input('Please choose an option to change: ').lower()
    if not settings_change:
        return print(CLEAR)
    if settings_change not in config.config.keys():  # you can manually change the set if you really want to
        return print(f'{C.red}That is not a valid option.{C.end}')
    if type(config.config[settings_change]) is bool:
        config.config[settings_change] = not config.config[settings_change]
    else:
        new_option = input('What do you want to change it to (enter full path for set_directory): ')
        config.config[settings_change] = new_option
    config.save_config(config.config)
    print(f'{CLEAR}{C.green}All changes saved!')


def new_set() -> None:
    print(f'{CLEAR}{C.green}GreatStudier study set creator.{C.end}\n')
    set_name = input('Name of the set: ')
    if not set_name:
        return print(f'{CLEAR}Aborted.')
    for c in ILLEGAL_FILENAME_CHARS:
        set_name.replace(c, '_')
    data = []
    print(f'{C.darkgreen}Press [Enter] to exit.{C.end}')
    while True:
        term = input('Enter a term: ')
        definition = input('Enter a definition: ')
        if not (term and definition):
            print('Finishing!')
            break
        data.append(utils.KeyData(term, definition, -1, 0))
        print()
    print(CLEAR)
    if data:
        utils.save_words(data, set_name)
        print(f'{C.green}Set successfully created!{C.end}')


def edit_mode(words) -> None:
    print(f'{CLEAR}{C.yellow}Terms\n{C.magenta}Number{C.end}: {C.green}Term{C.end} -> {C.darkblue}Definition{C.end}')
    print('--------------------------')
    for i in range(len(words)):
        print(f'{C.magenta}{i}{C.end}: {C.green}"{words[i].word}"{C.end} -> {C.darkblue}"{words[i].definition}"{C.end}')
    print()
    mode = input(f'{C.darkgreen}Enter a mode [+] add terms, [-] remove terms, or [e]dit terms: {C.end}')
    if not mode:
        return print(CLEAR)
    print(f'{C.darkgreen}Press [Enter] to exit.{C.end}')
    if mode in {'e', 'edit'}:
        while True:
            edit_num = input('Enter the number you want to edit (Blank to quit): ')
            if not edit_num:
                break
            edit_term = input('Enter the new term (Blank to keep term): ')
            edit_def = input('Enter the new definition (Blank to keep definition): ')
            if edit_term:
                words[int(edit_num)].word = edit_term
            if edit_def:
                words[int(edit_num)].definition = edit_def
            print()
        print(CLEAR)
    elif mode in {'+', 'add'}:
        while True:
            term = input('Enter a term: ')
            definition = input('Enter a definition: ')
            if not (term and definition):
                print('Finishing!')
                break
            words.append(utils.KeyData(term, definition, -1, 0))
            print()
        print(CLEAR)
    elif mode in {'-', 'remove'}:
        while True:
            if len(words) == 1:
                print(f'{CLEAR}{C.yellow}You may not remove a set with 1 term.{C.end}')
                break
            remove_num = input('Enter the number you want to remove (Blank to quit): ')
            if not remove_num:
                break
            remove_confirm = input(f'Are you sure you want to remove term {C.bwhite}{words[int(remove_num)].word}{C.end} [Y/n]. ')
            if remove_confirm.lower() != 'y':
                print('Aborted!')
                break
            del words[int(remove_num)]
    utils.save_words(words, config.config['set'])
    print(f'{C.green}All changes saved!{C.end}')


def main():
    print(f'{CLEAR}{C.green}GreatStudier Version {VERSION}{C.end}\n{motd.random()}{C.end}\n')
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
                      '[U]pload (NotImplemented)\n'
                      '[D]ownload (NotImplemented)\n'
                      '[C]hoose Set\n'
                      '[M]odify Set\n'
                      '[N]ew Set\n'
                      '[O]ptions\n'
                      '[S]tats\n'
                      '[Q]uit\n'
                      f'{C.darkblue}>{C.end} ')
            word_set = config.config['set']
            words = utils.load_words(word_set)
            print(f'{C.blue}Current set{C.end}: {C.bwhite}{word_set}{C.end}')
            new_terms, review_terms = utils.get_studyable(words)
        cmd = input(prompt).lower().strip()

        if cmd in {'quit', 'q'}:
            print('Exiting...')
            break
        # begin learning available
        if cmd in {'learn', 'l'} and learning_available:
            learn(words, new_terms)
        elif cmd in {'review', 'r'} and learning_available:
            review(words, review_terms)
        elif cmd in {'wipe', '_wipe_progress', 'w'} and learning_available:
            wipe_progress(words)
        elif cmd in {'modify', 'm'} and learning_available:
            edit_mode(words)
        elif cmd in {'upload', 'u'} and learning_available:
            url, deletion = uploads.upload_set(words, config.config['set'])
            print(f'{C.cyan}{url}{C.end} - Uploaded! {C.black}({deletion}){C.end}')
        # end learning available
        elif cmd in {'choose', 'c'}:
            choose_set()
        elif cmd in {'new', 'n'}:
            new_set()
        elif cmd in {'options', 'o'}:
            open_settings()
        elif cmd in {'stats', 's'}:
            stats()
        else:
            print(f'{CLEAR}That is not an option.\n')
        print(f'{C.green}GreatStudier{C.end}')

    gamify.fix_level(print_stuff=True)
    if config.config['show_gamify']:
        gamify.show_level()
    # SAVE STUFF
    gamify.save_gamify(gamify.gamify_data)
    config.save_config(config.config)


if __name__ == '__main__':
    main()
