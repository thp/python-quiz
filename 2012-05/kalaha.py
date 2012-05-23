#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# kalaha - Generic game core of my Kalaha implementation
# 2012-05-23 Thomas Perl <m@thp.io>
#

class Constants:
    INITIAL_SEEDS = 3
    HOUSES_PER_PLAYER = 6
    PLAYERS = 2

class Player:
    def __init__(self, id):
        self.id = id
        self.store = None
        self.houses = []

    @property
    def name(self):
        return 'Player %d' % (self.id+1)

class Pit:
    HOUSE, STORE = range(2)

    def __init__(self, game, player, pit=HOUSE):
        self.game = game
        self.player = player
        self.pit = pit
        self.seeds = (Constants.INITIAL_SEEDS if pit == Pit.HOUSE else 0)

        self.idx = -1
        self.next = None
        self.prev = None
        self.opposite = None

        if pit == Pit.STORE:
            # Register this pit as the player's store
            assert player.store is None
            player.store = self
        else:
            # Register this pit as a player's house
            player.houses.append(self)

    @property
    def is_store(self):
        return self.pit == Pit.STORE

    @property
    def is_empty(self):
        return self.seeds == 0

    def take(self):
        """Take all seeds and start dropping them

        Returns True if the player may play again, False otherwise
        """
        assert self.seeds > 0

        taken, self.seeds = self.seeds, 0

        return self.next.drop(taken, self.player)

    def steal_from(self, pit):
        """Steal all seeds from "pit" into this store

        pit - The (opponent's pit) to steal from
        """
        assert self.is_store
        assert not pit.is_store
        assert not pit.is_empty
        assert self.player != pit.player

        self.game.show_message('Stole %d seeds.' % pit.seeds)

        self.seeds, pit.seeds = self.seeds + pit.seeds, 0

    def drop(self, remaining, dropping_player):
        """
        remaining - How many seeds still need to be dropped
        dropping_player - Which player drops the seeds
        """
        was_empty = (self.seeds == 0)

        # Do not drop seeds into opponent's store
        if self.is_store and self.player != dropping_player:
            return self.next.drop(remaining, dropping_player)

        self.seeds, remaining = self.seeds + 1, remaining - 1

        if not remaining:
            if dropping_player == self.player:
                if self.is_store:
                    # The player gets an additional move
                    self.game.show_message('You get an additional move.')
                    return True

                if was_empty and not self.opposite.is_empty:
                    # The field stays empty
                    # (the seed we just put moves into the store)
                    self.player.store.seeds += 1
                    self.seeds = 0

                    # Steal the opposite seeds (if any)
                    self.player.store.steal_from(self.opposite)

            return False

        return self.next.drop(remaining, dropping_player)

class Game:
    TAKE, NEXT, PREV, SELECT, QUIT = range(5)

    def __init__(self):
        self.players = [Player(x) for x in range(Constants.PLAYERS)]
        self.pits = list(self.dig_pits())
        self.connect_pits()
        self.check_pits()
        self.messages = []

        self.current_player = 0
        self.game_over = False

    def draw(self, selected=-1):
        """Draw the current game

        selected - The index of the currently-selected pit (if any)
        """
        pass

    def input(self, player):
        """Get next input action as (action, data)-tuple

        player - the currently-selected player

        Expected return values:
            (TAKE, None)
            (NEXT, None)
            (PREV, None)
            (SELECT, index)
            (QUIT, None)

        You can also return None for "None of the above"
        """
        pass

    def notify(self, messages):
        """Show messages to the user

        messages - A list of messages to show to the user
        """
        pass

    def check_game_over(self):
        # If for any player, all houses are empty, the game is over
        if any(all(house.is_empty for house in player.houses)
                for player in self.players):
            # Move all remaining house seeds into players' stores
            for player in self.players:
                for house in player.houses:
                    player.store.seeds += house.seeds
                    house.seeds = 0

            self.show_message('Game over.')
            self.game_over = True

    def run(self):
        selected = 0

        def next(step=0):
            result = (selected + step) % len(self.pits)

            if step == 0:
                step = 1

            while (self.pits[result].player !=
                    self.players[self.current_player] or
                    self.pits[result].is_store or
                    self.pits[result].is_empty):
                result = (result + step) % len(self.pits)

            return result

        while True:
            self.draw(selected)
            input = self.input(self.players[self.current_player])
            if input is None:
                continue

            action, data = input

            if action in (Game.TAKE, Game.SELECT):
                if action == Game.SELECT:
                    # User-selected pit - validate if it's possible at all
                    old_selected, selected = selected, data
                    if next() != selected:
                        self.watch_messages()
                        self.show_message('You cannot select this pit.')
                        selected = old_selected
                        self.draw()
                        self.unwatch_messages()
                        continue

                pit = self.pits[selected]

                self.watch_messages()
                again = pit.take()
                self.draw()
                self.unwatch_messages()

                self.watch_messages()
                self.check_game_over()
                self.draw()
                self.unwatch_messages()

                if self.game_over:
                    break

                if not again:
                    self.next_player()

                selected = next()
            elif action == Game.NEXT:
                selected = next(1)
            elif action == Game.PREV:
                selected = next(-1)
            elif action == Game.QUIT:
                break

    def next_player(self):
        self.current_player = (self.current_player + 1) % Constants.PLAYERS

    def watch_messages(self):
        self.messages = []

    def unwatch_messages(self):
        if self.messages:
            self.notify(self.messages)

        self.messages = None

    def show_message(self, message):
        if self.messages is None:
            print '  ', inred(message)
        else:
            self.messages.append(message)

    def dig_pits(self):
        for player in self.players:
            for i in range(Constants.HOUSES_PER_PLAYER+1):
                if i == Constants.HOUSES_PER_PLAYER:
                    yield Pit(self, player, Pit.STORE)
                else:
                    yield Pit(self, player, Pit.HOUSE)

    def connect_pits(self):
        for idx, pit in enumerate(self.pits):
            pit.idx = idx
            pit.prev = self.pits[(idx-1) % len(self.pits)]
            pit.next = self.pits[(idx+1) % len(self.pits)]
            if not pit.is_store:
                pit.opposite = self.pits[len(self.pits) - 2 - idx]

    def check_pits(self):
        for pit in self.pits:
            assert pit.prev.next == pit
            assert pit.next.prev == pit

            if pit.is_store:
                assert pit.opposite is None
                assert pit.player != pit.next.player
            else:
                assert pit.opposite.opposite == pit
                assert pit.player == pit.next.player

