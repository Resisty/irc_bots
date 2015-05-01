#!/usr/bin/python
# =======================================
#
#  File Name : runbot.py
#
#  Purpose :
#
#  Creation Date : 30-04-2015
#
#  Last Modified : Thu 30 Apr 2015 11:15:08 PM CDT
#
#  Created By : Brian Auron
#
# ========================================
import sys
import yaml
import testirc

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
    kwargs['channels'] = [channel for channel in yml['channels']]
    bot = testirc.IRC(**kwargs)
    bot.run()

if __name__ == '__main__':
    main()
