#!/usr/bin/python
# -*- coding: utf-8 -*-
# kalaha_web - Web UI for Kalaha
# 2012-05-23 Thomas Perl <m@thp.io>

import kalaha

import BaseHTTPServer
import SocketServer
import shutil
import threading
import time
import json
import urlparse
import string
import random

def generate_id():
    return ''.join(random.choice(string.hexdigits) for _ in range(16))

class Event:
    DRAW, MESSAGE, REQUEST_INPUT, INPUT = range(4)

    EVENT_IDS = {
        DRAW: 'draw',
        MESSAGE: 'message',
        REQUEST_INPUT: 'request-input',
    }

    def __init__(self, id, data=None):
        self.id = id
        self.data = data

    def post(self, wfile, player_id):
        if self.id not in self.EVENT_IDS:
            # Don't send incoming events
            return

        if self.data.get('player_id', player_id) != player_id:
            # Don't send events destined for another player
            return

        print 'sending %s -> player %d' % (self.EVENT_IDS[self.id], player_id)

        data = 'event: %s\ndata: %s\n\n' % (
            self.EVENT_IDS[self.id],
            json.dumps(self.data)
        )
        wfile.write(data)

class EventQueue:
    def __init__(self):
        self.events = []

    def push(self, event):
        self.events.append(event)

class EventReader:
    def __init__(self, queue):
        self.queue = queue
        self.index = 0

    def pull(self):
        for i in range(self.index, len(self.queue.events)):
            self.index = i + 1
            yield self.queue.events[i]

    def wait_for(self, event_id):
        while True:
            for event in self.pull():
                if event.id == event_id:
                    return event

            time.sleep(.1)

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse.urlparse(self.path).query
        parameters = urlparse.parse_qs(query)

        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            shutil.copyfileobj(open('index.html'), self.wfile)
        elif self.path.startswith('/input'):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')

            data = {
                'input_id': parameters['id'][0],
                'index': parameters['index'][0],
            }
            print 'received input: %s' % data
            event_queue.push(Event(Event.INPUT, data))
        elif self.path.startswith('/events'):
            self.send_response(200)
            self.send_header('Content-type', 'text/event-stream')
            self.end_headers()
            player_id = int(parameters['player'][0])
            print 'player id connected:', player_id
            reader = EventReader(event_queue)
            while True:
                for event in reader.pull():
                    event.post(self.wfile, player_id)
                time.sleep(.1)

class ThreadingHTTPServer(SocketServer.ThreadingMixIn,
        BaseHTTPServer.HTTPServer):
    pass

class Game(kalaha.Game):
    def __init__(self, event_queue):
        kalaha.Game.__init__(self)
        self.event_queue = event_queue
        self.event_reader = EventReader(event_queue)

    def draw(self, selected=-1):
        data = {
            'players': [
                {
                    'store': self.players[i].store.seeds,
                    'houses': [{'index': h.idx, 'seeds': h.seeds, 'player': i}
                        for h in self.players[i].houses],
                }
                for i in range(kalaha.Constants.PLAYERS)
            ],
            'selected': selected,
        }
        self.event_queue.push(Event(Event.DRAW, data))

    def input(self, player):
        input_id = generate_id()
        data = {'input_id': input_id, 'player_id': player.id}
        self.event_queue.push(Event(Event.REQUEST_INPUT, data))

        while True:
            event = self.event_reader.wait_for(Event.INPUT)
            if event.data['input_id'] == input_id:
                return (kalaha.Game.SELECT, int(event.data['index']))

    def notify(self, messages):
        data = {'messages': messages, 'player_id': self.current_player}
        self.event_queue.push(Event(Event.MESSAGE, data))

if __name__ == '__main__':
    event_queue = EventQueue()
    game = Game(event_queue)

    server = ThreadingHTTPServer(('', 8080), RequestHandler)
    threading.Thread(target=server.serve_forever).start()

    game.run()

