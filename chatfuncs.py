#!/usr/bin/python
# =======================================
#
#  File Name: chatfuncs.py
#
#  Purpose: Provides functions f(regex, data) returning modified data for IRC
#           to send messages. Data and regex are mapped to these functions in
#           mapping.py.
#           all functions must obey signature:
#           def func(data, re.match):
#           where 'data' is a dictionary from irc.Message().classify()
#           To make things easier on the IRC bot, functions should return:
#           data['msg'] = [list of strings]
#           data['reply'] = 'public' or 'private'
#             public: to channel (will be a whisper if original message was
#             whispered)
#             private: whisper
#
#  Creation Date: 01-05-2015
#
#  Last Modified: Fri 01 May 2015 0120:39 PM CDT
#
#  Created By: Brian Auron
#
# ========================================

import random
import requests
import json

def manatee_maybe(data, match):
    if data['msg'] == data['msg'].upper() and len(data['msg']) > 4:
        manatee = random.randint(1, 33)
        data['msg'] = ['http://calmingmanatee.com/img/manatee{0}.jpg'.format(manatee)]
    else:
        data['msg'] = []
    data['reply'] = 'public'
    return data

def enhance(data, match):
    data['msg'] = ['/me types furiously. "Enhance."']
    data['reply'] = 'emote'
    return data

def fuck_off(data, match):
    data['msg'] = [':C']
    data['reply'] = 'public'
    return data

def cortana(data, match):
    data['msg'] = ['http://i0.kym-cdn.com/photos/images/original/000/837/637/7d6.gif']
    data['reply'] = 'public'
    return data

def windows_error(data, match):
    code = match.groups()[0]
    roll = random.randint(1, 1000)
    data['msg'] = ['Suggested course of action for code {0}: '.format(code)]
    if roll < 150:
        data['msg'][0] += 'install your choice of linux distro.'
    elif roll >= 150 and roll < 160:
        data['msg'][0] += 'have you tried Dragonfly BSD?'
    else:
        data['msg'][0] += 'turn it off and on again.'
    data['reply']
    return data

def happy_birthday(data, match):
    nick = data['nick']
    data['msg'] = ['Go {nick}, it\'s your birthday! Go {nick}, it\'s your birthday!']
    data['msg'].append('You\'re one year older, one year wiser, you\'re a rock \'n roll star, king, czar and kaiser!')
    data['msg'].append('You\'re the man of the hour, the VIP! You get the first slice -- of the P-I-E!')
    data['msg'].append('So blow out your candles and make a wish!')
    data['msg'].append('Put a smile on -- \'cuz it\'s your birthday, bitch!')
    data['msg'].append('Go {nick}, it\'s your birthday! Go {nick}, it\'s your birthday!')
    data['msg'] = [i.format(nick = nick) for i in data['msg']]
    data['reply'] = 'public'
    return data

def come_to_portland(data, match):
    data['msg'] = ['http://imgur.com/29Mr0h']
    data['reply'] = 'public'
    return data

def come_to_seattle(data, match):
    data['msg'] = ['http://i.imgur.com/Lwo0CTF.gif']
    data['reply'] = 'public'
    return data

def come_to_cleveland(data, match):
    data['msg'] = ['https://www.youtube.com/watch?v=ysmLA5TqbIY']
    data['reply'] = 'public'
    return data

def roll_dice(data, match):
    dicestr = match.groups()[1]
    modifiers = match.groups()[5].split()
    print modifiers
    if not modifiers:
        modifiers = [0]
    else:
        modifiers = [int(m) for m in modifiers]
    if not dicestr:
        data['msg'] = [str(random.randint(1, 6))]
    else:
        dice_sets = dicestr.split()
        results = []
        for dice_set in dice_sets:
            nums = dice_set.split('d')
            number = int(nums[0])
            size = int(nums[1])
            val = sum([random.randint(1, size) for i in range(number)])
            val += sum(modifiers)
            results.append('{0}: {1}'.format(dice_set, str(val)))
        data['msg'] = [', '.join(results)]
    data['reply'] = 'public'
    return data

def spin_wheel(data, match):
    values = range(5, 105, 5)
    data['msg'] = [str(random.choice(values))]
    data['reply'] = 'public'
    return data

def butts_me(data, match):
    who = match.groups()[0]
    if who != 'me':
        data['nick'] = who
    what = match.groups()[1]
    what = what.replace(' ', '%20')
    url = 'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={0}'
    url = url.format(what)
    results = requests.get(url)
    jdata = json.loads(results.text)
    try:
        data['msg'] = [jdata['data']['image_original_url']]
    except (TypeError, KeyError) as e:
        data['msg'] = ['That\'s a stupid search!']
    data['reply'] = 'public'
    return data

def urban(data, match):
    who = match.groups()[0]
    if who != 'me':
        data['nick'] = who
    what = match.groups()[1]
    what = what.replace(' ', '%20')
    which = match.groups()[2]
    if which:
        which = int(match.groups()[2].strip().split('#')[1]) - 1
    else:
        which = 0
    url = 'http://api.urbandictionary.com/v0/define?term={0}'
    url = url.format(what)
    results = requests.get(url)
    jdata = json.loads(results.text)
    if jdata['result_type'] == 'no_results':
        data['msg'] = ['That\'s a stupid search!']
    else:
        try:
            data['msg'] = jdata['list'][which]['definition'].split('\r\n')
        except IndexError as e:
            data['msg'] = ['No such definition number!']
    data['reply'] = 'public'
    return data

def haddaway(data, match):
    data['msg'] = ['Baby don\'t hurt me!  https://www.youtube.com/watch?v=Ktbhw0v186Q']
    data['reply'] = 'public'
    return data

def can_bobi_spend(data, match):
    data['msg'] = ['http://brianauron.info/CanBobiSpendThisMoney']
    data['reply'] = 'public'
    return data

def fixit(data, match):
    data['msg'] = ['https://www.youtube.com/watch?v=8ZCysBT5Kec']
    data['reply'] = 'public'
    return data

def good_sludge(data, match):
    strings = ['When I am drinking coffee, I always say, "I am going to have another sip of that!" after every sip.',
               'When I wake up in the morning, the first thing I do is stick my head out my window and yell, "Now it is time for me to drink coffee, the bean-based drink that you can find at the store!"',
               'I refer to the act of drinking coffee as "getting my sludge on."',
               'My daughter\'s full legal name is Sludge Junky, The Amazing Coffee-Worshipping Girl, and I require her to speak in the third person.',
               'If I go even one hour without getting my sludge on I become belligerent, and I say cruel and unforgivable things such as, "I like it when helpful people get carsick."',
               'My body is so amped up on caffeine that doctors have informed me that if my head ever got chopped off by a guillotine, the caffeine in my bloodstream would keep my decapitated body alive long enough for it to pick up my own severed head and punt it over the horizon.',
               'My favorite thing that I like to do is look at coffee and say, "Now I\'m looking at it."',
               'Whenever I see a dog on the street, I hold a coffee mug underneath its mouth for a little bit just in case it\'s the kind of dog that squirts hot jets of coffee out of its mouth.',
               'The surgery that doctors must perform to extract a person\'s entire body from a travel-size French press is named after me.',
               'My dream husband is a silent man standing perfectly still in the middle of the woods holding a handful of coffee beans in his clenched fist, and when I kiss him on the cheek, he opens up his hand so that I can look at the beans.',
               'I once drank so much coffee that a man said to me, "Whoa, buddy, slow down."',
               'My mother no longer speaks to me because I gave my father\'s eulogy while wearing a T-shirt that said "I\'m Just An Old Curmudgeon Who Loves To Get His Sludge On."',
               'There is a movie about my life called Often: The Frequency Of Coffee.',
               'When I see a baby, I will walk right up to that baby and whisper, "Coffee is the sludge I am after" right in that baby\'s ear.',
               'I was once on trial for murder, and 12 different courtroom stenographers got carpal tunnel syndrome from typing the phrase "Your Honor, coffee is the good sludge" so many times.',
               'I once wrote a 900-page epic poem called "Sheer Ecstasy" in which I rhymed "French press" with "bench press" over 15,000 times. It was the only rhyme in the poem.',
               'The New York Times has already written an article titled "Skeleton Of Nation\'s Greatest Burden Found Floating In Septic Tank Filled With Coffee," which it will run on the day that I die.']
    data['msg'] = [random.choice(strings)]
    data['reply'] = 'public'
    return data

def whelps(data, match):
    data['msg'] = ['WHELPS','LEFT SIDE','EVEN SIDE',
                   'MANY WHELPS','NOW','HANDLE IT!']
    data['reply'] = 'public'
    return data

def this_is_fine(data, match):
    data['msg'] = ['http://gunshowcomic.com/648']
    data['reply'] = 'public'
    return data
