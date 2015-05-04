#!/usr/bin/python
# =======================================
#
#  File Name : snorts.py
#
#  Purpose :
#
#  Creation Date : 03-05-2015
#
#  Last Modified : Sun 03 May 2015 08:14:25 PM CDT
#
#  Created By : Brian Auron
#
# ========================================

import peewee
import yaml
from playhouse.postgres_ext import PostgresqlExtDatabase
from datetime import date, datetime, timedelta

with open('panicbutt2.yaml', 'r') as fptr:
    cfg = yaml.load(fptr.read())
dbuser = cfg['dbuser']
dbpass = cfg['dbpass']
db = cfg['db']
psql_db = PostgresqlExtDatabase(db, user = dbuser, password = dbpass)

class Snorts(peewee.Model):
    nick = peewee.CharField()
    day = peewee.DateField()
    count = peewee.IntegerField(default = 0)

    class Meta:
        database = psql_db

def create_snorts():
    psql_db.connect()
    psql_db.create_tables([Snorts])

def drop_snorts():
    psql_db.connect()
    psql_db.drop_tables([Snorts])

def do_snort(nick):
    psql_db.connect()
    day = date.today()
    try:
        row = Snorts.select().where((Snorts.nick == nick) &
                                    (Snorts.day == day)).get()
    except peewee.DoesNotExist as e:
        row = Snorts.create(nick = nick, day = day)
    Snorts.update(count = Snorts.count + 1).where(Snorts.id == row.id).execute()
    row = Snorts.select().where(Snorts.id == row.id).get()
    psql_db.close()
    return '{0} has snorted {1} snorts today.'.format(row.nick, row.count)

def snort_me(data, match):
    who = match.groups()[0]
    if who == 'me':
        who = data['nick']
    nicks = data['nicks']()
    if who not in nicks:
        data['msg'] = ['Cannot snort {0} a snort, nick not in channel.'.format(who)]
    else:
        data['msg'] = [do_snort(who)]
    data['reply'] = 'public'
    return data

def show_snorts(data, match):
    day = date.today()
    rows = Snorts.select().where(Snorts.day == day)
    results = []
    for row in rows:
        results.append('{0} has snorted {1} snorts today.'.format(row.nick, row.count))
    if results == []:
        results.append('Nobody has snorted a snort today!')
    data['msg'] = results
    data['reply'] = 'public'
    return data
