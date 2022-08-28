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
from set_manager import choose_set, open_settings, new_set, edit_mode
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


def download_set():
    link = input('Link: ')
    try:
        result, name = uploads.download_set(link)
    except RuntimeError as e:
        print(f'{C.yellow}{e}{C.end}')
    else:
        dest = input('Save to (leave blank for default name): ')
        if not dest:
            dest = name
        utils.save_data(result, dest)


def main():
    print(f'{CLEAR}{C.green}GreatStudier Version {VERSION}{C.end}\n'
          f'{motd.random()}\n'
          f'{gamify.dashboard()}\n')
    while True:
        if config.config['set'] is None:
            learning_available = False
            prompt = (f'{C.darkred}It seems you do not have a set chosen!{C.end}\n'
                      f'{C.no}[L]earn{C.end}               {C.no}[R]eview{C.end}\n'
                      f'{C.no}[U]pload Set{C.end}          [D]ownload Set\n'
                      f'[C]hoose Set          [N]ew Set             {C.no}[M]odify Set{C.end}\n'
                      f'[O]ptions             [S]tats               {C.no}[W]ipe Progress{C.end}\n'
                      f'[Q]uit\n'
                      f'{C.darkblue}>{C.end} ')
        else:
            learning_available = True
            prompt = ('[L]earn               [R]eview\n'
                      '[U]pload Set          [D]ownload Set\n'
                      '[C]hoose Set          [N]ew Set             [M]odify Set\n'
                      '[O]ptions             [S]tats               [W]ipe Progress\n'
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
            print('Uploading...')
            url, deletion = uploads.upload_set(words, config.config['set'])
            print(f'{CLEAR}{C.cyan}{url}{C.end} - Uploaded! {C.black}({deletion}){C.end}')
        # end learning available
        elif cmd in {'download', 'd'}:
            download_set()
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

    if config.config['show_gamify']:
        gamify.fix_level(print_stuff=True)
        gamify.show_level()
    # SAVE STUFF
    gamify.save_gamify(gamify.gamify_data)
    config.save_config(config.config)


if __name__ == '__main__':
    main()
