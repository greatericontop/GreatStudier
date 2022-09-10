"""
Damerau-Levenshtein distance.

This is an inline version of the rapidfuzz library's Damerau-Levenshtein code.
It was included inline mainly to make compiling to a binary easier. Many unnecessary parts were removed.

It was copied at version 2.6.1, found here:
  https://github.com/maxbachmann/RapidFuzz/blob/v2.6.1/src/rapidfuzz/distance/DamerauLevenshtein_py.py
"""

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

# Copyright (C) 2022 Max Bachmann
# MIT License


def _damerau_levenshtein_distance_zhao(s1, s2):
    maxVal = max(len(s1), len(s2)) + 1
    last_row_id = {}
    last_row_id_get = last_row_id.get
    size = len(s2) + 2
    FR = [maxVal] * size
    R1 = [maxVal] * size
    R = [x for x in range(size)]
    R[-1] = maxVal

    for i in range(1, len(s1) + 1):
        R, R1 = R1, R
        last_col_id = -1
        last_i2l1 = R[0]
        R[0] = i
        T = maxVal

        for j in range(1, len(s2) + 1):
            diag = R1[j - 1] + (s1[i - 1] != s2[j - 1])
            left = R[j - 1] + 1
            up = R1[j] + 1
            temp = min(diag, left, up)

            if s1[i - 1] == s2[j - 1]:
                last_col_id = j  # last occurence of s1_i
                FR[j] = R1[j - 2]  # save H_k-1,j-2
                T = last_i2l1  # save H_i-2,l-1
            else:
                k = last_row_id_get(s2[j - 1], -1)
                l = last_col_id

                if (j - l) == 1:
                    transpose = FR[j] + (i - k)
                    temp = min(temp, transpose)
                elif (i - k) == 1:
                    transpose = T + (j - l)
                    temp = min(temp, transpose)

            last_i2l1 = R[j]
            R[j] = temp

        last_row_id[s1[i - 1]] = i

    dist = R[len(s2)]
    return dist


def distance(s1, s2, *, processor=None, score_cutoff=None):
    if processor is not None:
        s1 = processor(s1)
        s2 = processor(s2)

    dist = _damerau_levenshtein_distance_zhao(s1, s2)
    return dist if (score_cutoff is None or dist <= score_cutoff) else score_cutoff + 1


def similarity(s1, s2, *, processor=None, score_cutoff=None):
    if processor is not None:
        s1 = processor(s1)
        s2 = processor(s2)

    maximum = max(len(s1), len(s2))
    dist = distance(s1, s2)
    sim = maximum - dist
    return sim if (score_cutoff is None or sim >= score_cutoff) else 0


def normalized_distance(s1, s2, *, processor=None, score_cutoff=None):
    if processor is not None:
        s1 = processor(s1)
        s2 = processor(s2)

    maximum = max(len(s1), len(s2))
    dist = distance(s1, s2)
    norm_dist = dist / maximum if maximum else 0
    return norm_dist if (score_cutoff is None or norm_dist <= score_cutoff) else 1


def normalized_similarity(s1, s2, *, processor=None, score_cutoff=None):
    if processor is not None:
        s1 = processor(s1)
        s2 = processor(s2)

    norm_dist = normalized_distance(s1, s2)
    norm_sim = 1.0 - norm_dist
    return norm_sim if (score_cutoff is None or norm_sim >= score_cutoff) else 0
