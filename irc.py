#!/usr/bin/python
# =======================================
#
#  File Name : irc.py
#
#  Purpose : Be an IRC bot and handle messages appropriately
#
#  Creation Date : 30-04-2015
#
#  Last Modified : Thu 15 Oct 2015 05:44:32 PM CDT
#
#  Created By : Brian Auron
#
# ========================================
import socket
import re
import copy
import mapping
import sys
import threading, Queue
import time
import datetime

RECV_BYTES = 2 ** 12

class IRC(object):
    def __init__(self, server, port, nick, user, channel, rejoin=False, password = None):
        self.nick = nick
        self.user = user
        self.channel = channel
        self.password = password
        self.data = {'nick': self.nick, 'msg': '',
                     'type': None, 'channel': self.channel,
                     'reply': 'public', 'nicks': self.getnicks}
        self.host = server, port
        self.rejoin = rejoin
        self.queue = Queue.Queue()

    def queue_thread(self):
        self.send_thread = threading.Thread(target = self.socket_send)
        self.send_thread.daemon = True
        self.send_thread.start()

    def connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(self.host)
        self.setnick()
        self.setuser()
        self.join()
        self.queue_thread()

    def socket_send(self):
        while True:
            try:
                msg = self.queue.get_nowait()
            except Queue.Empty:
                time.sleep(0.1)
                continue
            print 'Sending msg to socket: "{}"'.format(msg)
            self._socket.send(msg)
            time.sleep(0.8)

    def put(self, msg):
        self.queue.put_nowait(msg)

    def send_command(self, command, *args, **kwargs):
        try:
            data = kwargs.pop('data')  # python2 kludge
        except KeyError:
            data = None
        args = [command] + list(args)
        if data:
            args.append(data)
        msg = ' '.join(args) + '\r\n'
        print 'Putting msg in queue: "{}"'.format(msg)
        self.put(msg)

    def setnick(self):
        self.send_command('NICK', self.nick)

    def setuser(self):
        self.send_command('USER', self.user, self.user, self.user, data = 'Python IRC')

    def join(self):
        joinstr = self.channel
        if self.password:
            joinstr += ' {}'.format(self.password)
        self.send_command('JOIN', joinstr)

    def chunk_message(self, line):
        n = 400 # Assuming 510 character messages plus channel, nick, and
                # punctuation, this should fit easily.
        return [line[i:i+n] for i in range(0, len(line), n)]


    def manhandle_data(self):
        self.data['msg'] = self._socket.recv(RECV_BYTES)
        now = str(datetime.datetime.now())
        print '[{}] Got data: "{}"'.format(now, self.data['msg'])
        # Do way more clever shit here, like (re)import msg_funcs or something
        self.classify()
        # allow perusal of channels if need be
        if self.data['type'] is None:
            return
        if self.data['type'] == 'PING':
            self._socket.send(self.data['msg'])
            return
        if self.data['type'] == 'PRIVMSG' and self.data['channel'] == self.nick:
            # private msg outside of channel
            self.get_replies()
            for reply in self.data['msg']:
                # reply is a dictionary like self.data's initialization, but
                # with actual data
                for msg in reply['msg']:
                    for line in self.chunk_message(msg):
                        print 'Private message to {}: {}'.format(reply['nick'], line)
                        self.send_command('PRIVMSG', reply['nick'], data = line)
            return
        if self.data['type'] == 'PRIVMSG':
            # do nothing until we have fun stuff to do
            self.get_replies()
            for reply in self.data['msg']:
                # reply is a dictionary like self.data's initialization, but
                # with actual data
                for msg in reply['msg']:
                    for line in self.chunk_message(msg):
                        if reply['reply'] == 'public':
                            self.send_command('PRIVMSG', reply['channel'],
                                              data = u':{}: {}'.format(reply['nick'], line))
                        elif reply['reply'] == 'private':
                            self.send_command('PRIVMSG', reply['nick'], data = line)
                        elif reply['reply'] == 'emote':
                            self.send_command('PRIVMSG', reply['channel'], data = line)
            return
        return

    def reload_map(self):
        print 'Reloading!'
        reload(mapping)
        retval = {}
        retval['msg'] = ['Reloaded']
        retval['reply'] = 'public'
        retval['channel'] = self.data['channel']
        retval['nick'] = self.data['nick']
        print 'retval in reload_map: "{0}"'.format(retval)
        return [retval]

    def get_replies(self):
        if self.data['msg'] == '{0} reload'.format(self.nick).lower():
            self.data['msg'] = self.reload_map()
            return
        tmp = []
        for regex, stuff in mapping.mapping.iteritems():
            case = re.IGNORECASE if stuff['i'] else 0
            match = re.search(regex, self.data['msg'], case)
            if match:
                data = dict(self.data)
                tmp.append(stuff['func'](data, match))
        self.data['msg'] = tmp

    def run(self, blocking=True):
        while blocking:
            self.manhandle_data()

    def getnicks(self):
        self.send_command('NAMES', self.channel)
        nickdata = self._socket.recv(RECV_BYTES)
        nickdata = nickdata.split('\r\n')
        for line in nickdata:
            if not line:
                continue
            # nicks come after a colon after a space after the channel name
            nicks = line.split(self.channel, 1)[1].strip(': ')
            for nick in nicks.split():
                # strip out op and voice modes
                yield nick.lstrip('@+')

    def replace_data(self, nick='', msg='', typ='', channel=''):
        self.data['nick'] = nick
        self.data['msg']= msg
        self.data['type'] = typ
        self.data['channel'] = channel

    def classify(self):
        parts = self.data['msg'].split(':')
        if parts[0].strip() == 'PING':
            retstr = 'PONG {0}\r\n'.format(parts[1])
            self.replace_data(parts[1], retstr, 'PING', None)
            return
        try:
            user, msgtype, channel = parts[1].strip().split()
        except IndexError as e:
            # probably got a QUIT and now we have empty data
            print 'Quitting for now, do clever stuff later.'
            sys.exit(1)
        except ValueError as e:
            # handle kicks if we want
            try:
                user, msgtype, channel, me = parts[1].strip().split()
                if msgtype == 'KICK' and self.rejoin:
                    self.join()
            except ValueError as e:
                pass

            # otherwise, probably system messages at startup, ignore them
            self.replace_data()
            return
        if msgtype != 'PRIVMSG':
            # ignore it for now
            self.replace_data()
            return
        match = re.search('([\w-]+)!', user)
        try:
            nick = match.groups()[0]
        except AttributeError as e:
            print 'Something fucked up: {0}'.format(e)
            self.replace_data()
            return
        msg = ' '.join(parts[2:]).strip()
        typ = 'PRIVMSG'
        if channel == nick:
            # don't spam yourself/channel
            self.replace_data()
            return
        self.replace_data(nick, msg, typ, channel)
        return
