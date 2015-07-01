#!/usr/bin/python3

# -*- coding: utf-8 -*-

# Copyright (C) 2015 ibu@radempa.de
#
# Permission is hereby granted, free of charge, to
# any person obtaining a copy of this software and
# associated documentation files (the "Software"),
# to deal in the Software without restriction,
# including without limitation the rights to use,
# copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is
# furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission
# notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
# OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""
solution to https://pyug.at/action/diff/PythonDojo/Ziffernkette

Only one of in general more possible solutions is calculated.
The algorithm is not optimized. It involves recursion.

Basic idea:

* start on the left-hand side of the result (most significant digits)
* numbers can be grouped according to their initial digits
* all groups can be handled separately, with initial digits ordered 9,...,1
* within a group numbers (or rather strings) can be compared pairwise
  to obtain an optimal number (the one to be chosen next)
* when comparing, these cases may occur::

  * both numbers are equal: keep the current optimum
  * both numbers have same length: choose the bigger one
  * both numbers have differing length and when cutting
    both to their minimum length one is bigger: choose
    the bigger one (regardless of whether it is the longer
    or shorter one)
  * both numbers have differing length and the longer one
    begins with the same digits as the shorter one:
    in this case we have to try padding the shorter one
    with the optimum of all remaining numbers (i.e., 
    except itself), which which involves recursion
"""


def group_by_first_char(strs):
    """
    Group a list of strings *strs* by their first character.

    Return a dict mapping the first character to a
    list of all strs beginning with this character.

    All strings in *strs* must have length > 0.
    """
    groups = {}
    for s in strs:
        char0 = s[0]
        if char0 not in groups:
            groups[char0] = []
        groups[char0].append(s)
    return groups


def order_num_strs(l):
    """
    Order a list *l* of strings beginning with the same digit.

    The strings will be ordered such that the string
    formed by concatenating them in the reuslting order
    will be the maximal possible integer.
    """
    result = []
    remaining = l
    while len(remaining) > 0:
        chosen = choose_optimal(remaining)
        result.append(chosen)
        ind = remaining.index(chosen)
        del remaining[ind]
    return result


def choose_optimal(nums):
    """
    From a list of number strings *nums* choose the optimal one.

    The number strings are assumed to have the same initial digit.
    The optimal one is that which leads to the biggest result, see
    :func:`order_num_strs`.
    """
    optimal = nums[0]
    if len(nums) == 1:
        return optimal
    for s in nums[1:]:
        r = compare(optimal, s, nums)
        if r:
            optimal = s
    return optimal


def compare(s1, s2, s_all):
    l1, l2 = len(s1), len(s2)
    if l1 == l2:
        return s2 > s1
    mi = min(l1, l2)
    if s1[:mi] > s2[:mi]:
        return False
    if s1[:mi] < s2[:mi]:
        return True
    # padding the shorter string with the optimal remaining one
    if l1 < l2:
        shorter = s1
        longer = s2
    else:
        shorter = s2
        longer = s1
    all_without_shorter = s_all.copy()
    ind = all_without_shorter.index(shorter)
    del all_without_shorter[ind]
    padding = choose_optimal(all_without_shorter)
    if l1 < l2:
        s1x = (s1 + padding)[:l2]
        s2x = s2
    else:
        s1x = s1
        s2x = (s2 + padding)[:l1]
    return s2x > s1x


def run(input):
    num_strs = [str(i) for i in input]
    #print('Input list:')
    #for s in sorted(num_strs):
    #    print('       ', s)
    digit_groups = group_by_first_char(num_strs)
    ordered_num_strs = []
    for d in reversed(range(1,10)):
        digit0 = str(d)
        if digit0 in digit_groups:
            l = digit_groups[digit0]
            ordered_num_strs += order_num_strs(l)
    #print('Ordered list:', ' '.join(ordered_num_strs))
    result = int(''.join(ordered_num_strs))
    #print('Maximal int: ', result)
    return result


if __name__ == '__main__':
    input = [71, 71, 75, 778, 7572, 758, 7588, 7, 78, 7575, 7778, 771, 778, 777, 7771, 7770, 7777]
    #input = [99, 9, 81, 71, 71, 75, 7572, 758, 7588, 7, 78, 221, 21, 21]
    run(input)
