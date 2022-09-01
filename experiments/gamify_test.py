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

import gamify


def main():
    for lvl in [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150]:
        gamify.gamify_data = {'level': lvl, 'xp': 11222}
        print(gamify.prestige())


if __name__ == '__main__':
    main()
