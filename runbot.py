#!/usr/bin/python
# =======================================
#
#  File Name : runbot.py
#
#  Purpose :
#
#  Creation Date : 30-04-2015
#
#  Last Modified : Mon 04 May 2015 01:26:46 PM CDT
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
        kwargs['rejoin'] = yml['rejoin']
    except KeyError as e:
        kwargs['rejoin'] = False
    bot = irc.IRC(**kwargs)
    bot.run()

if __name__ == '__main__':
    main()
