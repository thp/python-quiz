#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Reversi Kata for Python Quiz 2013-04
# Thomas Perl <m@thp.io>; 2013-03-23

import collections
import re

Point = collections.namedtuple('Point', ('x', 'y'))


def parse_board(board):
    """Parse an input string into a (list_of_rows, player)-tuple

    The board must be 8x8, the player a single character.
    Leading and trailing whitespace is trimmed, empty lines ignored.
    """
    rows = []
    player = None

    for row in filter(None, map(str.strip, board.splitlines())):
        if len(row) == 8:
            assert all(c in ('B', 'W', '.') for c in row), 'Invalid character'
            rows.append(row)
            assert len(rows) <= 8, 'More than 8 rows found'
        elif len(row) == 1:
            assert player is None, 'Player is set multiple times'
            player = row
            assert player in ('B', 'W'), 'Player must be either B or W'
        else:
            raise ValueError('Invalid input line')

    return rows, player


# All possible directions
STEPS = [-1, 0, +1]
DIRECTIONS = [Point(x, y) for x in STEPS for y in STEPS if not x == y == 0]

class Reversi:
    def __init__(self, board):
        self.board, self.player = parse_board(board)

    def find_player_positions(self):
        for y, row in enumerate(self.board):
            for x, field in enumerate(row):
                if field == self.player:
                    yield Point(x, y)

    def inside_board(self, pos):
        return pos.x >= 0 and pos.y >= 0 and pos.x < 8 and pos.y < 8

    def make_trace(self, pos, direction):
        """Trace from pos towards direction

        Returns a generator containing (pos, field)-tuples starting at
        pos and ending at the first empty field or at the board border
        """
        while self.inside_board(pos):
            field = self.board[pos.y][pos.x]
            yield pos, field

            if field == '.':
                break

            pos = Point(pos.x + direction.x, pos.y + direction.y)

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
            position, field = trace[-1]
            yield position

    def apply_trace(self, trace):
        # Positions to which to write the player's chars
        positions = [pos for pos, field in trace]

        # New board is the old board, with some fields overwritten
        self.board = [
                ''.join(field if (x, y) not in positions else self.player
                    for x, field in enumerate(row))
            for y, row in enumerate(self.board)]

        # New player is the opponent
        self.player = ('B' if self.player == 'W' else 'W')

    def problem(self):
        """Returns a string representation of the problem"""
        return '\n'.join(self.board + [self.player])

    def solution(self):
        """Returns a string representation of the solution"""
        destinations = set(self.find_destinations())

        def generate():
            for y, row in enumerate(self.board):
                for x, field in enumerate(row):
                    if (x, y) in destinations:
                        yield '0'
                    else:
                        yield field
                yield '\n'

        return ''.join(generate()).strip()

    def fields(self):
        """Returns a string with possible solutions as field names"""
        return ('ABCDEFGH'[x] + '12345678'[y]
                for x, y in sorted(set(self.find_destinations())))

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

