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

import atexit
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
from set_manager import choose_set, new_set, edit_mode
from constants import *

try:
    # Linux only, patches input to allow "fancy" editing
    # Will fail on Windows and OS X
    import readline as _
except ModuleNotFoundError:
    pass


def exit_task():
    gamify.save_gamify(gamify.gamify_data)
    config.save_config(config.config)
def handle_terminate_signal(sig, frame):
    print(f'\n{C.red}Exiting...')
    sys.exit(0)
signal.signal(signal.SIGINT, handle_terminate_signal)
signal.signal(signal.SIGTERM, handle_terminate_signal)
atexit.register(exit_task)


def learn(words, new_terms) -> None:
    if not new_terms:
        print(f'{C.yellow}Nothing to do!{C.end}')
        input(CONTINUE)
        print(CLEAR)
        return
    random.shuffle(new_terms)
    print(f'{CLEAR}{C.green}LEARN: Type each term once to continue.{C.end}\n')
    amount = min(NEW_CHUNK_SIZE, len(new_terms))
    print(f'You are ready to:\nLEARN x{C.darkcyan}{amount}{C.end}\n')
    study_indices = list(range(amount))
    for i in study_indices:
        key = new_terms[i]
        question = key.definition
        answer = key.word
        if utils.answer_mode(config.config['answer_with']) == utils.answer_mode.DEFINITION:
            question = key.word
            answer = key.definition
        print(f'\n\n{C.yellow}{answer} {C.green}= {C.darkyellow}{question}{C.end}')
        while True:
            if input().strip().lower() == answer.lower():
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
    utils.save_words(words, config.config['set'])
    print('You are done!')
    gamify.increment_login_bonus()
    gamify.gamify_data['xp'] += 20 if amount == NEW_CHUNK_SIZE else 10  # session bonus
    input(CONTINUE)
    print(CLEAR)


def review(words, review_terms) -> None:
    if not review_terms:
        print(f'{C.yellow}Nothing to do!{C.end}')
        input(CONTINUE)
        print(CLEAR)
        return
    random.shuffle(review_terms)
    amount = min(REVIEW_CHUNK_SIZE, len(review_terms))
    print(f'{CLEAR}You are ready to:\nREVIEW x{C.darkcyan}{amount}{C.end}\n')
    for i in range(amount):
        key = review_terms[i]
        if quiz.quiz(key):
            gamify.increment_review_correct()  # in addition to other increments
    utils.save_words(words, config.config['set'])
    print('You are done!')
    gamify.increment_login_bonus()
    gamify.gamify_data['xp'] += 45 if amount == REVIEW_CHUNK_SIZE else 25  # session bonus
    input(CONTINUE)
    print(CLEAR)


def study(words) -> None:
    if not words:
        print(f'{C.yellow}Nothing to do!{C.end}')
        input(CONTINUE)
        print(CLEAR)
        return
    words = words.copy()  # maintain references to the actual elements, but shuffling them won't affect the other one
    random.shuffle(words)
    total = len(words)
    print(f'{CLEAR}You are ready to:\nSTUDY x{C.darkcyan}{total}{C.end}\n')
    for i, word in enumerate(words):
        quiz.quiz(word, extra=f'#{i + 1}/{total} ', increment_knowledge_level=False)
    print('You are done!')
    gamify.increment_login_bonus()
    gamify.gamify_data['xp'] += 20 if total >= 10 else 5  # session bonus
    input(CONTINUE)
    print(CLEAR)


def stats() -> None:
    data = gamify.gamify_data
    print(CLEAR)
    print(f'{gamify.dashboard()}\n')
    print(f'{C.yellow}STATISTICS{C.end}')
    print(f"{C.green}You have {data['correct_answers']} correct answers.{C.end}")
    print(f"{C.red}You have {data['wrong_answers']} wrong answers.{C.end}")
    if data['wrong_answers'] != 0:
        print(f"Answer Ratio: {data['correct_answers'] / data['wrong_answers']:.2f}")
    print(f'{C.cyan}Skill Score: {gamify.get_skill()}{C.end}')
    print(f'{C.magenta}You have studied for {C.green}{gamify.dashboard_time_studied()}{C.magenta}.{C.end}')
    gamify.print_quest_progress()
    print(f"\n{C.green}You're currently level {gamify.dashboard()}\n")
    input(CONTINUE)
    print(CLEAR)


def wipe_progress(words) -> None:
    confirm = input(f'{C.red}Clearing ALL progress for this set?{C.end} [y/N]: ')
    if confirm not in YES_DEFAULT_NO:
        print(CLEAR)
        return
    for key in words:
        key.last_covered = -1
        key.repetition_spot = 0
    utils.save_words(words, config.config['set'])
    print(f'{C.green}Successfully deleted all progress in your current set!{C.end}')
    input(CONTINUE)
    print(CLEAR)


def upload_set(words) -> None:
    print(CLEAR)
    print('Uploading...')
    if config.config['paste_api_key']:
        if config.config['paste_username']:
            try:
                set_id = uploads.find_set(config.config['set'])
            except uploads.FailedRequestError as e:
                print(f'{C.yellow}Failed to find set! {e}{C.end}')
            else:
                if set_id is not None:
                    consent = input('Found a paste on account; edit and update it? [Y/n]: ').strip().lower()
                    if consent in YES_DEFAULT_YES:
                        uploads.edit_set(words, set_id)
                        print(f'{C.cyan}https://paste.gg/{set_id}{C.end} - Uploaded and updated!')
                        input(CONTINUE)
                        print(CLEAR)
                        return
        else:
            print(f"{C.yellow}You haven't set your username in the config! This is required due to limitations in the API.{C.end}")
    else:
        print(f"{C.yellow}You haven't set an API key! Use one to group all your uploads under one account.{C.end}")
    try:
        url, deletion = uploads.upload_set(words, config.config['set'])
    except uploads.FailedRequestError as e:
        print(f'{C.red}Failed to upload set! {e}{C.end}')
    else:
        print(f'{C.cyan}{url}{C.end} - Uploaded! {C.black}({deletion}){C.end}')
    input(CONTINUE)
    print(CLEAR)


def download_set() -> None:
    print(CLEAR)
    link = input('Link: ')
    if not link:
        print(f'{C.red}Nothing was provided!{C.end}')
        input(CONTINUE)
        print(CLEAR)
        return
    try:
        result, name = uploads.download_set(link)
    except uploads.FailedRequestError as e:
        print(f'{C.red}Failed to download set! {e}{C.end}')
        input(CONTINUE)
        print(CLEAR)
        return
    dest = input(f'Download to ({name}): ')
    if not dest:
        dest = name
    utils.save_data(result, dest)
    print(f'{C.green}Set downloaded successfully.{C.end}')
    input(CONTINUE)
    print(CLEAR)


def open_settings() -> None:
    print(CLEAR)
    settings = f'{C.yellow}OPTIONS{C.end}\n'
    for key, value in config.config.items():
        if key == 'set':
            continue
        if key == 'paste_api_key' and value is not None:
            value = value[:4] + '**********'
        if key == 'answer_with' and value is not None:
            value = utils.answer_mode(value).name
        # distinguish between the actual None and a string called that
        if value is None:
            value = '<None>'
        settings += f'{C.green}{key}{C.end} = {C.darkblue}{value}{C.end}\n'
    print(settings)
    while True:
        settings_change = input('Option to change: ').lower()

        if not settings_change:
            print(f'{C.red}Nothing was provided!{C.end}')
            break

        if settings_change == 'reset':
            if input('Do you really want to reset the config? [Y/n]: ') in YES_DEFAULT_YES:
                config.config = config.update_with_defaults()
        elif settings_change == 'answer_with':
            if config.config[settings_change] is None:
                config.config[settings_change] = 0
            config.config[settings_change] = (config.config[settings_change] + 1) % 2
            print(f'Value set to {C.bwhite}{utils.answer_mode(config.config[settings_change]).name}{C.end}.\n')
        elif settings_change not in config.config:
            print(f'{C.red}That is not a valid option.{C.end}\n')
        elif type(config.config[settings_change]) is bool:
            config.config[settings_change] = not config.config[settings_change]
            print(f'Toggled option to {C.bwhite}{config.config[settings_change]}{C.end}.\n')
        else:
            new_value = input('New value: ')
            if not new_value:
                new_value = None
            config.config[settings_change] = new_value
            print(f'Value set to {C.bwhite}{new_value}{C.end}.\n')
    config.reload_config()
    config.save_config(config.config)
    print(f'{C.green}All changes saved!{C.end}')
    input(CONTINUE)
    print(CLEAR)


def main():
    os.system('')  # enables windows ANSI escape
    print(f'{CLEAR}{C.green}GreatStudier Version {VERSION}{C.end}\n'
          f'{motd.random()}\n'
          f'{gamify.dashboard()}\n')
    if VERSION.endswith('nightly'):
        print(f'{C.yellow}You are using a nightly build, which may be unstable.{C.end}\n')
    while True:
        gamify.update_quests()
        gamify.fix_level(print_stuff=True)
        if config.config['set'] is None:
            learning_available = False
            prompt = (f'{C.darkred}It seems you do not have a set chosen!{C.end}\n'
                      f'{C.no}[L]earn{C.end}               {C.no}[R]eview{C.end}              {C.no}[S]tudy{C.end}\n'
                      f'{C.no}[U]pload Set{C.end}          [D]ownload Set        [C]hoose Set\n'
                      f'[N]ew Set             {C.no}[M]odify Set{C.end}          [O]ptions\n'
                      f'[St]ats               {C.no}[W]ipe Progress{C.end}       [Q]uit\n'
                      f'{C.darkblue}>{C.end} ')
        else:
            learning_available = True
            prompt = (f'[L]earn               [R]eview              [S]tudy\n'
                      f'[U]pload Set          [D]ownload Set        [C]hoose Set\n'       
                      f'[N]ew Set             [M]odify Set          [O]ptions\n'
                      f'[St]ats               [W]ipe Progress       [Q]uit\n'
                      f'{C.darkblue}>{C.end} ')
            word_set = config.config['set']
            words = utils.load_words(word_set)
            print(f'{C.blue}Current set{C.end}: {C.bwhite}{word_set}{C.end}')
            new_terms, review_terms = utils.get_studyable(words)
        cmd = input(prompt).lower().strip()

        if cmd in {'quit', 'q'}:
            gamify.fix_level(print_stuff=True)
            gamify.show_level()
            sys.exit(0)
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
            upload_set(words)
        # end learning available
        elif cmd in {'download', 'd'}:
            download_set()
        elif cmd in {'quizlet', 'qu'}:
            convert_quizlet_set()
        elif cmd in {'choose', 'c'}:
            choose_set()
        elif cmd in {'new', 'n'}:
            new_set()
        elif cmd in {'options', 'o'}:
            open_settings()
        elif cmd in {'stats', 'st'}:
            stats()
        else:
            print(f'{CLEAR}{C.red}That is not an option.{C.end}')
        print(f'{C.green}GreatStudier{C.end}')


if __name__ == '__main__':
    main()
