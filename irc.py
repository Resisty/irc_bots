#!/usr/bin/python
# =======================================
#
#  File Name : irc.py
#
#  Purpose : Be an IRC bot and handle messages appropriately
#
#  Creation Date : 30-04-2015
#
#  Last Modified : Fri 01 May 2015 12:04:33 AM CDT
#
#  Created By : Brian Auron
#
# ========================================
import socket
import re
#import chatfuncs

class IRC():
    def __init__(self, server, port, nick, user, channels):
        self.server = server
        self.port = port
        self.nick = nick
        self.user = user
        self.channels = channels
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect(( server, port ))
        self.irc.send('NICK {0}\r\n'.format(nick))
        self.irc.send('USER {0} {0} {0} :Python IRC\r\n'.format(user))
        for channel in channels:
            self.irc.send( 'JOIN {0}\r\n'.format(channel))

    def manhandle_data(self):
        self.data = self.irc.recv(4096)
        print self.data
        # Do way more clever shit here, like (re)import msg_funcs or something
        data = Message(self.data).classify()
        if data['type'] is None:
            return
        if data['type'] == 'PING':
            self.irc.send(data['msg'])
            return
        if data['type'] == 'PRIVMSG' and data['channel'] == self.nick:
            # private msg outside of channel
            retstr = 'PRIVMSG {0} :I\'m not smart enough for this shit yet.\r\n'.format(data['nick'])
            self.irc.send(retstr)
            return
        if data['type'] == 'PRIVMSG':
            # do nothing until we have fun stuff to do
            #retstr = 'PRIVMSG {0} :{1}\r\n'.format(data['channel'], FUNSTUFF_HERE)
            #self.irc.send(retstr)
            return
        return

    def run(self):
        while True:
            self.manhandle_data()

class Message():
    def __init__(self, data):
        self.parts = data.split()
        self.retval = {'nick': None, 'msg': None, 'type': None, 'channel': None}

    def fill_retval(self, nick = None, msg = None, typ = None, channel = None):
        self.retval['nick'] = nick
        self.retval['msg']= msg
        self.retval['type'] = typ
        self.retval['channel'] = channel
        return self.retval

    def classify(self):
        if self.parts[0] == 'PING':
            retstr = 'PONG {0}\r\n'.format(self.parts[1])
            return self.fill_retval(self.parts[1], retstr, 'PING', None)
        if self.parts[1] != 'PRIVMSG':
            # ignore it for now
            return self.fill_retval()
        match = re.search(':([\w-]+)!', self.parts[0])
        try:
            nick = match.groups()[0]
        except AttributeError as e:
            print 'Something fucked up: {0}'.format(e)
            return self.fill_retval()
        msg = self.parts[-1][1:] # lop off the colon
        channel = self.parts[2]
        typ = 'PRIVMSG'
        if channel == nick:
            # don't spam yourself/channel
            return self.fill_retval()
        return self.fill_retval(nick, msg, typ, channel)

