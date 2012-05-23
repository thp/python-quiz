#!/usr/bin/python
# -*- coding: utf-8 -*-
# kalaha_console - ANSI Terminal Frontend for Kalaha
# 2012-05-23 Thomas Perl <m@thp.io>

import os
import functools

incolor = lambda color_id, s: '\033[9%dm%s\033[0m' % (color_id, s)
inred, ingreen, inyellow, inblue = (functools.partial(incolor, x)
        for x in range(1, 5))

import kalaha

class Game(kalaha.Game):
    def draw(self, selected=-1):
        brackets = lambda i: (ingreen(' > %02d < ')
                if i==selected else ' [ %02d ] ')
        house = lambda i: brackets(i) % self.pits[i].seeds
        store = lambda i: inblue(house(self.players[i].store.idx))

        os.system('clear')
        print '\n'*3
        print ' '*13, ' '.join(house(i) for i in range(12, 6, -1))
        print ' '*7, store(1), ' '*47, store(0)
        print ' '*13, ' '.join(house(i) for i in range(0, 6))
        print '\n'*3

    def input(self, player):
        print inyellow(player.name)
        input = raw_input('([t]ake,[n]ext,[p]rev,[q]uit or index)> ')

        if input.isdigit():
            return (kalaha.Game.SELECT, int(input))

        if input in ('t', 'take'):
            return (kalaha.Game.TAKE, None)
        elif input in ('n', 'next'):
            return (kalaha.Game.NEXT, None)
        elif input in ('p', 'prev'):
            return (kalaha.Game.PREV, None)
        elif input in ('q', 'quit'):
            return (kalaha.Game.QUIT, None)

        return None

    def notify(self, messages):
        for message in messages:
            print '  ', inred(message)
        raw_input('\n(press enter to continue)')

if __name__ == '__main__':
    game = Game()
    game.run()

