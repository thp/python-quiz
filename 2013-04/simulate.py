#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Reversi versus game simulator

from __future__ import print_function

import reversi
import random

# Method for picking a move: random move, best (longest) move, worst (shortest) move
RANDOM, BEST, WORST = range(3)
method = WORST

sim = reversi.Reversi("""
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

steps = 0
while True:
    print(sim.problem())
    print()

    solutions = list(sim.find_traces())
    if not len(solutions):
        print('No more solutions. Game over:', sim.stats(), 'after', steps, 'steps')
        break

    if method == RANDOM:
        random.shuffle(solutions)
        solution = solutions[0]
    elif method == BEST:
        solution = sorted(solutions, key=len, reverse=True)[0]
    elif method == WORST:
        solution = sorted(solutions, key=len)[0]

    sim.apply_trace(solution)
    steps += 1

