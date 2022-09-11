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

import os
import random as _random

from constants import C


motd = [
    'Suckless!',
    'Free Software!',
    'Proprietary!',
    'eeeeeee',
    'Quizlet Sucks!',
    '20220825!',
    'Made with Python!',
    'New stuff soon\u2122',
    'Down with Big Brother!',
    'I would like to interject for a moment!',
    f'{C.red}C{C.darkyellow}o{C.yellow}l{C.green}o{C.darkgreen}r{C.cyan}m{C.blue}a{C.darkblue}t{C.darkmagenta}i{C.magenta}c{C.darkred}!{C.end}',
    'Now in 256 Colors!',
    'Remember to turn off your computer before 03:14:07 UTC on 1/19/2038.',
    'Study hard!',
    'You are an idiot ah hahahahahahahahahahahaha!',
    'Never gonna give you up!',
    'Everything is a file!',
    "It's pronounced char!",
    "No, Neo. I'm telling you that when you're ready, you won't have to.",
    'IlIllIIIlIllIIllIllIllI!',
    'As seen on TV!',
    'Skill issue!',
    'Where brain?',
    'January 1, 1970!',
    'I use Arch BTW!',
    f'{os.getpid()}!',
    'The more you ask, the longer I will take to update!',
    'No more p2w!',
    'Finally here!',
    'Boop!',
    'Free as in Freedom!',
    'ALL WRONGS RESERVED!',
    'Task failed successfully!',
    'Finally not beta anymore!',
    '99 bugs on the wall. Take one down, pass it around, 2147483647 bugs on the wall!',
    '6e 65 76 65 72 20 67 6f 6e 6e 61 20 67 69 76 65 20 79 6f 75 20 75 70!',
    'GREATSTUDIER IS GREAT!!!',
    'A binary is source code if you try hard enough!',
    'Your free trial of GreatStudier has expired!',
]


def random() -> str:
    return _random.choice(motd)

