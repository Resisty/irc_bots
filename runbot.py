#!/usr/bin/python
# =======================================
#
#  File Name : runbot.py
#
#  Purpose :
#
#  Creation Date : 30-04-2015
#
#  Last Modified : Fri 19 Jun 2015 02:42:55 PM CDT
#
#  Created By : Brian Auron
#
# ========================================
import sys
import yaml
import irc

def main():
    try:
        config = sys.argv[1]
    except:
        print 'I need a config file!'
        sys.exit(1)
    try:
        with open(config, 'r') as fptr:
            yml = yaml.load(fptr.read())
    except Exception as e:
        print 'Could not load config.yaml because: {0}'.format(e)
        sys.exit(1)
    kwargs = {}
    kwargs['nick'] = yml['nick']
    kwargs['server'] = yml['server']
    kwargs['port'] = yml['port']
    kwargs['user'] = yml['user']
    kwargs['channel'] = yml['channel']
    try:
        kwargs['password'] = yml['password']
    except KeyError:
        pass
    try:
        kwargs['rejoin'] = yml['rejoin']
    except KeyError as e:
        kwargs['rejoin'] = False
    bot = irc.IRC(**kwargs)
    bot.connect()
    bot.run(blocking=True)

if __name__ == '__main__':
    main()
