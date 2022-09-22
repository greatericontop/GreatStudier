"""Contains other helper functions to manage sets."""

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

import config
import utils
from constants import *


def add_term_interactively(word_data: list) -> None:
    """Add terms (interactively) to :word_data: and modify it IN PLACE."""
    while True:
        term = input('Enter a term: ')
        definition = input('Enter a definition: ')
        if not (term and definition):
            print('Finishing!')
            break
        word_data.append(utils.KeyData(term, definition, -1, 0))
        print()


def choose_set() -> None:
    sets = [p.name for p in config.get_set_directory().iterdir() if p.is_file()]
    print_sets = '\n'.join(sets)

    if not sets:
        print(f'\n{C.yellow}You currently have no sets available. Import or create a new set to continue.{C.end}')
        input(CONTINUE)
        print(CLEAR)
        return
    print(f'{CLEAR}{C.darkcyan}Available Study Sets{C.end}\n{print_sets}\n\n{C.darkgreen}Leave blank to exit.{C.end}')
    while True:
        word_set = input('Choose a set: ')
        if not word_set:
            config.config['set'] = None
            break
        if word_set in sets:
            config.config['set'] = word_set
            break
        print(f'{C.red}Invalid Set! Please choose a valid set.{C.end}')
    print(CLEAR)


def new_set() -> None:
    print(CLEAR)
    set_name = input('New set name: ')
    if not set_name:
        print(f'{C.red}Nothing was provided!{C.end}')
        return
    for c in ILLEGAL_FILENAME_CHARS:
        set_name.replace(c, '_')
    data = []
    add_term_interactively(data)
    if data:
        utils.save_words(data, set_name)
        print(f'{C.green}Set successfully created!{C.end}')
        input(CONTINUE)
    print(CLEAR)


def edit_mode(words) -> None:
    print(f'{CLEAR}{C.yellow}TERMS\n{C.magenta}Number{C.end}: {C.green}Term{C.end} -> {C.darkblue}Definition{C.end}')
    print('--------------------------')
    for i, key in enumerate(words):
        if key.repetition_spot == 0:
            extra_info = 'not learned'
        else:
            timeleft = int(key.last_covered + SPACED_REPETITION[key.repetition_spot] - time.time())
            if timeleft <= 0:
                extra_info = f'ready #{key.repetition_spot}'
            elif timeleft <= 86400:
                extra_info = f'in {timeleft//3600 % 24}h {timeleft//60 % 60}m{C.end}'
            else:
                extra_info = f'in {timeleft//86400}d {timeleft//3600 % 24}h {timeleft//60 % 60}m{C.end}'
        print(f'{C.magenta}{i}{C.end}: {C.green}"{key.word}"{C.end} -> {C.darkblue}"{key.definition}"{C.end} {C.darkwhite}({extra_info}){C.end}')
    mode = input(f'{C.darkgreen}[+] add terms, [-] remove terms, [E]dit terms, [R]ename set: {C.end}').lower()
    if mode in {'e', 'edit'}:
        print('Leave blank to exit.\n')
        while True:
            try:
                edit_num = int(input('Enter the number you want to edit: '))
            except ValueError:
                break
            if edit_num >= len(words):
                break
            edit_term = input(f'Enter the new term (blank to keep): ')
            edit_def = input(f'Enter the new definition (blank to keep): ')
            if edit_term:
                words[edit_num].word = edit_term
            if edit_def:
                words[edit_num].definition = edit_def
            print()
    elif mode in {'+', 'add'}:
        print('Leave blank to exit.\n')
        add_term_interactively(words)
    elif mode in {'-', 'remove'}:
        print('Leave blank to exit.\n')
        while True:
            if len(words) == 1:
                print(f'{CLEAR}{C.yellow}You may not remove a set with 1 term.{C.end}')
                break
            try:
                remove_num = int(input('Number to remove: '))
            except ValueError:
                break
            if remove_num >= len(words):
                break
            del words[remove_num]
    elif mode in {'rename', 'r'}:
        new_name = input('Enter a new name for the set: ')
        for c in ILLEGAL_FILENAME_CHARS:
            new_name.replace(c, '_')
        old_set_path = config.get_set_directory() / config.config['set']
        new_set_path = config.get_set_directory() / new_name
        old_set_path.rename(new_set_path)
        config.config['set'] = new_name
    else:
        print(f'{C.red}That is not an option.{C.end}')
        input(CONTINUE)
        print(CLEAR)
        return
    utils.save_words(words, config.config['set'])
    print(f'{C.green}All changes saved!{C.end}')
    input(CONTINUE)
    print(CLEAR)
