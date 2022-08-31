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

import config
import utils
from utils import C
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

    if len(sets) == 0:
        print(f'\n{C.yellow}You currently have no sets available. Import or create a new set to continue.{C.end}')
        input()
    else:
        print(f'{CLEAR}{C.darkcyan}Available Study Sets{C.end}\n{print_sets}\n\n{C.darkgreen}Leave blank to exit.{C.end}')
        while True:
            word_set = input('Choose a set: ')
            if not word_set:
                config.config['set'] = None
                break
            if word_set in sets:
                config.config['set'] = word_set
                break
            else:
                print(f'{C.red}Invalid Set! Please choose a valid set.{C.end}')


def new_set() -> None:
    print(f'{CLEAR}{C.green}GreatStudier study set creator.{C.end}\n')
    print('Leave blank to exit.\n')
    set_name = input('Name of the set: ')
    if not set_name:
        return print(f'{CLEAR}Aborted.')
    for c in ILLEGAL_FILENAME_CHARS:
        set_name.replace(c, '_')
    data = []
    add_term_interactively(data)
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
    mode = input(f'{C.darkgreen}Enter a mode [+] add terms, [-] remove terms, [e]dit terms, [r]ename set: {C.end}')
    if not mode:
        return print(CLEAR)
    print('Leave blank to exit.\n')
    if mode in {'e', 'edit'}:
        while True:
            try:
                edit_num = int(input('Enter the number you want to edit (Blank to quit): '))
            except ValueError:
                break
            if edit_num >= len(words):
                break
            edit_term = input('Enter the new term (Blank to keep term): ')
            edit_def = input('Enter the new definition (Blank to keep definition): ')
            if edit_term:
                words[edit_num].word = edit_term
            if edit_def:
                words[edit_num].definition = edit_def
            print()
        print(CLEAR)
    elif mode in {'+', 'add'}:
        add_term_interactively(words)
        print(CLEAR)
    elif mode in {'-', 'remove'}:
        while True:
            if len(words) == 1:
                print(f'{CLEAR}{C.yellow}You may not remove a set with 1 term.{C.end}')
                break
            try:
                remove_num = int(input('Enter the number you want to remove (Blank to quit): '))
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
    utils.save_words(words, config.config['set'])
    print(f'{C.green}All changes saved!{C.end}')
