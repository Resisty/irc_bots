#!/usr/bin/python
# =======================================
#
#  File Name : irc.py
#
#  Purpose : Be an IRC bot and handle messages appropriately
#
#  Creation Date : 30-04-2015
#
#  Last Modified : Thu 07 May 2015 11:43:09 PM CDT
#
#  Created By : Brian Auron
#
# ========================================
import socket
import re
import copy
import mapping
import sys

class IRC():
    def __init__(self, server,
                 port, nick,
                 user, channel,
                 byte = 4096, rejoin = False):
        self.server = server
        self.port = port
        self.nick = nick
        self.user = user
        self.channel = channel
        self.byte = byte
        self.data = {'nick': self.nick, 'msg': '',
                     'type': None, 'channel': self.channel,
                     'reply': 'public', 'nicks': self.getnicks}
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect(( self.server, self.port ))
        self.setnick()
        self.setuser()
        self.join()

    def setnick(self):
        self.irc.send('NICK {0}\r\n'.format(self.nick))

    def setuser(self):
        self.irc.send('USER {0} {0} {0} :Python IRC\r\n'.format(self.user))

    def join(self):
        self.irc.send('JOIN {0}\r\n'.format(self.channel))

    def manhandle_data(self):
        self.data['msg'] = self.irc.recv(self.byte)
        print 'Got data: "{0}"'.format(self.data['msg'])
        # Do way more clever shit here, like (re)import msg_funcs or something
        self.classify()
        # allow perusal of channels if need be
        if self.data['type'] is None:
            return
        if self.data['type'] == 'PING':
            self.irc.send(self.data['msg'])
            return
        if self.data['type'] == 'PRIVMSG' and self.data['channel'] == self.nick:
            # private msg outside of channel
            self.get_replies()
            for reply in self.data['msg']:
                # reply is a dictionary like self.data's initialization, but
                # with actual data
                for msg in reply['msg']:
                    retstr = 'PRIVMSG {0} :{1}\r\n'.format(reply['nick'], msg)
                    self.irc.send(retstr)
            return
        if self.data['type'] == 'PRIVMSG':
            # do nothing until we have fun stuff to do
            #retstr = 'PRIVMSG {0} :{1}\r\n'.format(data['channel'], FUNSTUFF_HERE)
            #self.irc.send(retstr)
            self.get_replies()
            for reply in self.data['msg']:
                # reply is a dictionary like self.data's initialization, but
                # with actual data
                for msg in reply['msg']:
                    if reply['reply'] == 'public':
                        retstr = 'PRIVMSG {0} :{1}: {2}\r\n'.format(reply['channel'],  reply['nick'], msg)
                        self.irc.send(retstr)
                    elif reply['reply'] == 'private':
                        retstr = 'PRIVMSG {0} : {1}\r\n'.format(reply['nick'], msg)
                        self.irc.send(retstr)
                    elif reply['reply'] == 'emote':
                        print 'Emoting.'
                        retstr = 'PRIVMSG {0} :{1}\r\n'.format(reply['channel'], msg)
            return
        return

    def reload_map(self):
        print 'Reloading!'
        reload(mapping)
        retval = copy.deepcopy(self.data)
        retval['msg'] = ['Reloaded']
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
                tmp.append(stuff['func'](copy.deepcopy(self.data), match))
        self.data['msg'] = tmp

    def run(self):
        while True:
            self.manhandle_data()

    def getnicks(self):
        msg = 'NAMES {0}\r\n'.format(self.channel)
        self.irc.send(msg)
        self.data = self.irc.recv(self.byte)
        self.data = self.data.split('\r\n')
        nicklist = []
        for line in self.data:
            if line == '':
                continue
            # nicks come after a colon after a space after the channel name
            nicks = line.split(self.channel)[1].strip()[1:].split()
            # strip out op and voice modes
            nicks = [re.sub('[@\+]', '', nick) for nick in nicks]
            nicklist += [nick for nick in nicks]

        return nicklist

    def replace_data(self, nick = '', msg = '', typ = '', channel = ''):
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
