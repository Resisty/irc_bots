#!/usr/bin/python
# =======================================
#
#  File Name : jeff.py
#
#  Purpose : Keep track of Jeff's level of existential crisis.
#
#  Creation Date : 01-05-2015
#
#  Last Modified : Fri 06 Nov 2015 12:55:37 PM CST
#
#  Created By : Brian Auron
#
# ========================================
import datetime
import bs4
import re
import peewee
import os
import yaml
from playhouse.postgres_ext import PostgresqlExtDatabase

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
yaml_loc = os.path.join(BASE_DIR, 'panicbutt2.yaml')
with open(yaml_loc, 'r') as fptr:
    cfg = yaml.load(fptr.read())
dbuser = cfg['dbuser']
dbpass = cfg['dbpass']
db = cfg['db']
psql_db = PostgresqlExtDatabase(db, user = dbuser, password = dbpass)

class JeffCrisis(peewee.Model):
    nick = peewee.CharField()
    datetime = peewee.DateTimeField()
    level = peewee.CharField()

    class Meta:
        database = psql_db

class Level(peewee.Model):
    name = peewee.TextField(unique = True)
    text = peewee.TextField(default = 'black')
    font = peewee.TextField(default = 'Lucida Console')
    bg = peewee.TextField(default = 'critical.gif')

    class Meta:
        database = psql_db

def create_crisis():
    psql_db.connect()
    psql_db.create_tables([JeffCrisis, Level])

def drop_crisis():
    psql_db.connect()
    psql_db.drop_tables([JeffCrisis, Level])

jeff_crisis_levels = {'critical' : {'text' : 'black',
                                    'font' : 'Lucida Console',
                                    'bg' : "critical.gif"},
                      'too damn high' : {'text' : 'red',
                                         'font' : 'Lucida Console',
                                         'bg' : "toodamnhigh.gif"},
                      'cat' : {'text' : 'white',
                                        'font' : 'Arial',
                                        'bg' : "expressive_cat.png"},
                      'can\'t even' : {'text' : 'purple',
                                       'font' : 'Impact',
                                       'bg' : "canteven.gif"},
                      'pants meat' : {'text' : 'pink',
                                      'font' : 'Times New Roman',
                                      'bg' : "pantsmeat.gif"},
                      'under control' : {'text' : 'yellow',
                                         'font' : 'Cursive',
                                         'bg' : "undercontrol.gif"},
                      'linuxpocalypse' : {'text' : 'green',
                                          'font' : 'Impact',
                                          'bg' : "tux.gif"}}

def get_current_level():
    recent = JeffCrisis.select().order_by(JeffCrisis.id.desc()).get()
    return recent.level.lower()

def set_crisis_level(nick, level):
    level = level.lower()
    link = "http://brianauron.info/jeff-existential-crisis-level/"
    if get_current_level() != level:
        psql_db.connect()
        JeffCrisis.create(nick = nick, datetime = datetime.datetime.now(), level = level)
        text = "Jeff's existential crisis level has been set to " + level
    else:
        text = "Jeff's existential crisis level is already {0}, ya jerk!".format(level)
    text += "\n{0}".format(link)
    return text

def til_sane():
    grad = datetime.date(2016, 5, 31)
    diff = grad - datetime.date.today()
    data = 'Assuming he sticks to the plan, Jeff becomes sane in {0} days.'.format(str(diff.days))
    return data

def jeff_info(data, match):
    verb = match.groups()[0]
    verbs = [i.name for i in Level.select()]
    if verb in verbs:
        data['msg'] = [set_crisis_level(data['nick'], verb)]
        data['msg'].append('http://brianauron.info/jeff-existential-crisis-level/')
    elif verb in ['list', 'enumerate', 'print']:
        data['msg'] = [', '.join(jeff_crisis_levels.keys())]
    elif verb in ['link', 'url']:
        data['msg'] = ['http://brianauron.info/jeff-existential-crisis-level/']
    elif verb in ['what is']:
        data['msg'] = [get_current_level()]
    elif verb in ['how long until', 'when will']:
        try:
            sanity = match.groups()[1]
            if not sanity:
                raise ValueError('Need a state of being for Jeff!')
        except (IndexError, ValueError) as e:
            data['msg'] = ['{0} Jeff what?'.format(verb.capitalize())]
        else:
            data['msg'] = [til_sane()]
    else:
        data['msg'] = ['{} Jeff what?'.format(verb.capitalize())]
    data['reply'] = 'public'
    return data
