"""Message of the day"""

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

from utils import C


motd = [
    'Suckless!',
    'Free Software!',
    'eeeeeee',
    'Quizlet Sucks',
    '20220825!',
    'Made using Python',
    'New stuff soon\u2122',
    'Down with Big Brother!',
    'I would like to interject for a moment!',
    f'{C.red}C{C.darkyellow}o{C.yellow}l{C.green}o{C.darkgreen}r{C.cyan}m{C.blue}a{C.darkblue}t{C.darkmagenta}i{C.magenta}c{C.darkred}!{C.end}',
    'Now in 256 Colors!',
    'Remember to turn off your computer before 03:14:07 UTC on 1/19/2038.',
    'Study hard',
    'You are an idiot ah hahahahahaha',
    'Never gonna give you up...'
]


def pick_random_motd() -> str:
    return random.choice(motd)
