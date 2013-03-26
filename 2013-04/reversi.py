#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Reversi Kata for Python Quiz 2013-04
# Thomas Perl <m@thp.io>; 2013-03-23

from __future__ import print_function

import collections
import re

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def inside_board(self):
        return self.x >= 0 and self.y >= 0 and self.x < SIZE and self.y < SIZE

    def exists_in(self, collection):
        for other in collection:
            if self.x == other.x and self.y == other.y:
                return True

        return False

SIZE = 8

# All possible directions
STEPS = [-1, 0, +1]
DIRECTIONS = [Point(x, y) for x in STEPS for y in STEPS if not x == y == 0]


def parse_board(board):
    """Parse an input string into a (list_of_rows, player)-tuple

    The board must be 8x8, the player a single character.
    Leading and trailing whitespace is trimmed, empty lines ignored.
    """
    rows = []
    player = None

    for row in filter(None, map(str.strip, board.splitlines())):
        if len(row) == SIZE:
            assert all(c in ('B', 'W', '.') for c in row), 'Invalid character'
            rows.append(list(row))
            assert len(rows) <= SIZE, 'More than 8 rows found'
        elif len(row) == 1:
            assert player is None, 'Player is set multiple times'
            player = row
            assert player in ('B', 'W'), 'Player must be either B or W'
        else:
            raise ValueError('Invalid input line')

    return rows, player

class Reversi:
    def __init__(self, board):
        self.board, self.player = parse_board(board)

    def find_player_positions(self):
        for y, row in enumerate(self.board):
            for x, field in enumerate(row):
                if field == self.player:
                    yield Point(x, y)

    def make_trace(self, pos, direction):
        """Trace from pos towards direction

        Returns a generator containing (pos, field)-tuples starting at
        pos and ending at the first empty field or at the board border
        """
        while pos.inside_board():
            field = self.board[pos.y][pos.x]
            yield pos, field

            if field == '.':
                break

            pos = pos.add(direction)

    def validate_trace(self, trace):
        """Checks if a trace is a valid move in Reversi

        Valid move means:
            1. Starting with a single player field
            2. One or more opponent fields
            3. Ending with a single empty field

        Returns True if it's a valid move, False otherwise.
        """
        trace_string = ''.join(field for position, field in trace)

        # We start with a single player field, then one or more fields that are
        # neither the player nor an empty field, and then a single empty field
        pattern = '^X[^X.]+[.]$'.replace('X', self.player)
        return re.match(pattern, trace_string) is not None

    def find_traces(self):
        """Find all possible traces for valid moves"""
        for pos in self.find_player_positions():
            for direction in DIRECTIONS:
                trace = list(self.make_trace(pos, direction))
                if self.validate_trace(trace):
                    yield trace


    def find_destinations(self):
        """Find all possible end position for valid moves"""
        for trace in self.find_traces():
            pos, field = trace[-1]
            yield pos

    def apply_trace(self, trace):
        # Overwrite trace with player's char
        for pos, field in trace:
            self.board[pos.y][pos.x] = self.player

        # New player is the opponent
        self.player = ('B' if self.player == 'W' else 'W')

    def problem(self):
        """Returns a string representation of the problem"""
        return '\n'.join([''.join(x) for x in self.board] + [self.player])

    def solution(self):
        """Returns a string representation of the solution"""
        destinations = list(self.find_destinations())

        def generate():
            for y, row in enumerate(self.board):
                for x, field in enumerate(row):
                    if Point(x, y).exists_in(destinations):
                        yield '0'
                    else:
                        yield field
                yield '\n'

        return ''.join(generate()).strip()

    def fields(self):
        """Returns a generator with possible solutions as field names"""
        return sorted('ABCDEFGH'[pos.x] + '12345678'[pos.y]
                for pos in self.find_destinations())

    def stats(self):
        def generate():
            for c in 'BW':
                count = sum(1 for row in self.board
                        for field in row if field == c)
                yield '%s=%d' % (c, count)

        return ', '.join(generate())

if __name__ == '__main__':
    reversi = Reversi("""
        ........
        ........
        ........
        ...BW...
        ...WB...
        ........
        ........
        ........
        B
    """)

    print()
    print('Problem:')
    print(reversi.problem())
    print()
    print('Solution:')
    print(reversi.solution())
    print()
    print('Fields:', ', '.join(reversi.fields()))
    print()
    print('Stats:', reversi.stats())
    print()

