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
import requests
import signal
import sys

import config
import gamify
import motd
import quiz
import uploads
import utils
from set_manager import choose_set, new_set, edit_mode
from utils import C
from constants import *

try:
    # Linux only, patches input to allow "fancy" editing
    # Will fail on Windows and OS X
    import readline as _readline
except ModuleNotFoundError:
    pass


def terminate_handler(sig, frame):
    print(f'\n{C.red}Exiting...')
    gamify.save_gamify(gamify.gamify_data)
    config.save_config(config.config)
    sys.exit(0)


signal.signal(signal.SIGINT, terminate_handler)
signal.signal(signal.SIGTERM, terminate_handler)


def learn(words, new_terms) -> None:
    if not new_terms:
        print(f'{C.yellow}Nothing to do!{C.end}')
        return
    random.shuffle(new_terms)
    print(f'{CLEAR}{C.green}LEARN: Type each term once to continue.{C.end}\n')
    amount = min(NEW_CHUNK_SIZE, len(new_terms))
    print(f'You are ready to:\nLEARN x{C.darkcyan}{amount}{C.end}\n')
    study_indices = list(range(amount))
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
    print(f'{CLEAR}You are done!')
    utils.save_words(words, config.config['set'])


def review(words, review_terms) -> None:
    if not review_terms:
        print(f'{C.yellow}Nothing to do!{C.end}')
        return
    random.shuffle(review_terms)
    amount = min(REVIEW_CHUNK_SIZE, len(review_terms))
    print(f'{CLEAR}You are ready to:\nREVIEW x{C.darkcyan}{amount}{C.end}\n')
    for i in range(amount):
        key = review_terms[i]
        quiz.quiz(key)
    print(f'{CLEAR}You are done!')
    utils.save_words(words, config.config['set'])


def study(words) -> None:
    if not words:
        print(f'{C.yellow}Nothing to do!{C.end}')
        return
    random.shuffle(words)
    total = len(words)
    print(f'{CLEAR}You are ready to:\nSTUDY x{C.darkcyan}{total}{C.end}\n')
    for i, word in enumerate(words):
        quiz.quiz(word, extra=f'#{i+1}/{total} ', increment_knowledge_level=False)
    print(CLEAR)


def stats() -> None:
    data = gamify.gamify_data
    print(f'{CLEAR}{C.green}Statistics{C.end}')
    print(f"{C.green}You have {data['correct_answers']} correct answers.{C.end}")
    print(f"{C.red}You have {data['wrong_answers']} wrong answers.{C.end}")
    if data['wrong_answers'] != 0:
        print(f"Answer Ratio: {data['correct_answers'] / data['wrong_answers']:.2f}")
    print(f'{C.cyan}Skill Score: {gamify.get_skill()}{C.end}')
    print(f"{C.green}You're currently level {gamify.dashboard()}\n\n")


def wipe_progress(words) -> None:
    print(f'{C.red}Clearing ALL progress for this set! Continue only if you are sure.{C.end}')
    input()
    for key in words:
        key.last_covered = -1
        key.repetition_spot = 0
    utils.save_words(words, config.config['set'])
    print(CLEAR)


def download_set() -> None:
    link = input('Link: ')
    if not link:
        print(f'{C.red}Nothing was provided!{C.end}')
        return
    try:
        result, name = uploads.download_set(link)
    except RuntimeError as e:
        print(f'{C.yellow}{e}{C.end}')
        return
    dest = input(f'Download to ({name}): ')
    if not dest:
        dest = name
    utils.save_data(result, dest)
    print(f'{CLEAR}{C.green}Set downloaded successfully.{C.end}')


def open_settings() -> None:
    settings = 'Options\n'
    for key, value in config.config.items():
        if key == 'set':
            continue
        if key == 'paste_api_key' and value is not None:
            value = value[:4] + '**********'
        settings += f'{C.darkgreen}{key}{C.end} = {C.darkgreen}{value}{C.end}\n'
    print(settings)
    settings_change = input('Option to change: ').lower()
    if not settings_change:
        return
    if settings_change not in config.config:  # you can manually change the set if you really want to
        print(f'{C.red}That is not a valid option.{C.end}')
        return
    if type(config.config[settings_change]) is bool:
        config.config[settings_change] = not config.config[settings_change]
        print(f'Toggled option to {config.config[settings_change]}.')
    else:
        new_value = input('New value: ')
        config.config[settings_change] = new_value
    config.reload_config()
    config.save_config(config.config)
    print(f'{CLEAR}{C.green}All changes saved!')


def main():
    # TODO: fix visually unappealing CLI
    os.system('')  # enables windows ANSI escape
    print(f'{CLEAR}{C.green}GreatStudier Version {VERSION}{C.end}\n'
          f'{motd.random()}\n'
          f'{gamify.dashboard()}\n')
    while True:
        if config.config['set'] is None:
            learning_available = False
            prompt = (f'{C.darkred}It seems you do not have a set chosen!{C.end}\n'
                      f'{C.no}[L]earn{C.end}               {C.no}[R]eview{C.end}              {C.no}[S]tudy{C.end}\n'
                      f'{C.no}[U]pload Set{C.end}          [D]ownload Set\n'
                      f'[C]hoose Set          [N]ew Set             {C.no}[M]odify Set{C.end}\n'
                      f'[O]ptions             [St]ats               {C.no}[W]ipe Progress{C.end}\n'
                      f'[Q]uit\n'
                      f'{C.darkblue}>{C.end} ')
        else:
            learning_available = True
            prompt = (f'[L]earn               [R]eview              [S]tudy\n'
                      f'[U]pload Set          [D]ownload Set\n'
                      f'[C]hoose Set          [N]ew Set             [M]odify Set\n'
                      f'[O]ptions             [St]ats               [W]ipe Progress\n'
                      f'[Q]uit\n'
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
        elif cmd in {'study', 's'} and learning_available:
            study(words)
        elif cmd in {'wipe', '_wipe_progress', 'w'} and learning_available:
            wipe_progress(words)
        elif cmd in {'modify', 'm'} and learning_available:
            edit_mode(words)
        elif cmd in {'upload', 'u'} and learning_available:
            print('Uploading...')
            try:
                url, deletion = uploads.upload_set(words, config.config['set'])
                print(f'{CLEAR}{C.cyan}{url}{C.end} - Uploaded! {C.black}({deletion}){C.end}')
            except requests.exceptions.ConnectionError:
                print(f'{CLEAR}{C.red}Connection error, unable to connect to paste.gg{C.end}')
        # end learning available
        elif cmd in {'download', 'd'}:
            try:
                download_set()
            except requests.exceptions.ConnectionError:
                print(f'{CLEAR}{C.red}Connection error, unable to connect to paste.gg{C.end}')
        elif cmd in {'choose', 'c'}:
            choose_set()
        elif cmd in {'new', 'n'}:
            new_set()
        elif cmd in {'options', 'o'}:
            open_settings()
        elif cmd in {'stats', 'st'}:
            stats()
        else:
            print(f'{CLEAR}That is not an option.')
        print(f'{C.green}GreatStudier{C.end}')

    if config.config['show_gamify']:
        gamify.fix_level(print_stuff=True)
        gamify.show_level()
    # SAVE STUFF
    gamify.save_gamify(gamify.gamify_data)
    config.save_config(config.config)


if __name__ == '__main__':
    main()
