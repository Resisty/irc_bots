#!/usr/bin/python
# =======================================
#
#  File Name : snorts.py
#
#  Purpose :
#
#  Creation Date : 03-05-2015
#
#  Last Modified : Thu 07 May 2015 11:25:27 PM CDT
#
#  Created By : Brian Auron
#
# ========================================

import functools
import yaml
import datetime

import peewee
from playhouse.postgres_ext import PostgresqlExtDatabase

with open('panicbutt2.yaml', 'r') as fptr:
    cfg = yaml.load(fptr.read())
dbuser = cfg['dbuser']
dbpass = cfg['dbpass']
db = cfg['db']
psql_db = PostgresqlExtDatabase(db, user=dbuser, password=dbpass)


class BaseModel(peewee.Model):
    class Meta:
        database = psql_db


class Snorts(BaseModel):
    nick = peewee.CharField()
    day = peewee.DateField()
    count = peewee.IntegerField(default=0)


class Counts(BaseModel):
    key = peewee.CharField(unique=True)
    count = peewee.IntegerField(default=0)


def connect(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    try:
      psql_db.connect()
      return func(*args, **kwargs)
    finally:
      psql_db.close()


@connect
def create_tables():
    psql_db.create_tables([Snorts, Counts])

@connect
def drop_tables():
    psql_db.connect()
    psql_db.drop_tables([Snorts, Counts])

@connect
def do_snort(nick):
    day = datetime.date.today()
    try:
        row = Snorts.select().where((Snorts.nick == nick) &
                                    (Snorts.day == day)).get()
    except peewee.DoesNotExist as e:
        row = Snorts.create(nick = nick, day = day)
    Snorts.update(count = Snorts.count + 1).where(Snorts.id == row.id).execute()
    row = Snorts.select().where(Snorts.id == row.id).get()
    return '{0} has snorted {1} snorts today.'.format(row.nick, row.count)

def snort_me(data, match):
    who = match.groups()[0]
    if who == 'me':
        who = data['nick']
    nicks = data['nicks']()  # wow this is hack-y
    if who not in nicks:
        data['msg'] = ['Cannot snort {0} a snort, nick not in channel.'.format(who)]
    else:
        data['msg'] = [do_snort(who)]
    data['reply'] = 'public'
    return data

@connect
def show_snorts(data, match):
    day = datetime.date.today()
    rows = Snorts.select().where(Snorts.day == day)
    results = []
    for row in rows:
        results.append('{0} has snorted {1} snorts today.'.format(row.nick, row.count))
    if results == []:
        results.append('Nobody has snorted a snort today!')
    data['msg'] = results
    data['reply'] = 'public'
    return data

@connect
def count_update(data, match):
  key, delta = match.groups()
  delta = {'++': 1, '--': -1}[delta]
  with psql_db.atomic():
    try:
      count = Count.create(key = key, count = 0)
    except peewee.IntegrityError:
      count = Count.get(Count.key == key)
    count.count += delta
    count.save()
    return '{} is now {}'.format(key, count.count)

@connect
def count_get(data, match):
  key = match.group(0)
  try:
    return str(Count.get(Count.key == key))
  except peewee.DoesNotExist:
    return 'None'
