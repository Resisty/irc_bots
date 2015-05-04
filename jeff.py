#!/usr/bin/python
# =======================================
#
#  File Name : jeff.py
#
#  Purpose : Keep track of Jeff's level of existential crisis.
#
#  Creation Date : 01-05-2015
#
#  Last Modified : Sun 03 May 2015 09:03:50 PM CDT
#
#  Created By : Brian Auron
#
# ========================================
import datetime
import bs4
import re

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
    try:
        with open('/var/www/html/jeff-existential-crisis-level/jeff-existential-crisis-level.html',
                  'r') as fptr:
            html = fptr.read()
            soup = bs4.BeautifulSoup(html)
    except IOError as e:
        return 'Could not read file. Check permissions and try again.'
    level = soup.find('h1').string.lower()
    return level

def edit_html(level):
    color = jeff_crisis_levels[level]['text']
    bgimg = jeff_crisis_levels[level]['bg']
    font = jeff_crisis_levels[level]['font']
    htmlfile = '/var/www/html/jeff-existential-crisis-level/index.html'
    try:
        with open(htmlfile, 'r') as fptr:
            html = fptr.read()
    except IOError as e:
        return 'Could not read file. Check permissions and try again.'
    soup = bs4.BeautifulSoup(html)
    style = soup.find('style')
    ustr = unicode(style.string)
    subber = r'\1{0}\3'.format(bgimg)
    nustr = re.sub('(img\/)(.*)(\))', subber, ustr)
    style.string = nustr
    try:
        with open(htmlfile, 'w') as fptr:
            fptr.write(str(soup))
    except IOError as e:
        return 'Could not write file. Check permissions and try again.'

    htmlfile = '/var/www/html/jeff-existential-crisis-level/jeff-existential-crisis-level.html'
    try:
        with open(htmlfile, 'r') as fptr:
            html = fptr.read()
    except IOError as e:
        return 'Could not read file. Check permissions and try again.'
    soup = bs4.BeautifulSoup(html)
    h1 = soup.find('h1')
    h1.attrs = {u'style': u'font-weight: bold; font-size: 120pt; font-family: Arial, sans-serif; text-decoration: none; color: white;',
                u'class': [u'text-center'],
                u'title': u'level'}
    style = re.sub('(font-family: )([\w\s]+)', r'\1{0}'.format(font), h1.attrs['style'])
    style = re.sub('(color: )(\w+)', r'\1{0}'.format(color), style)
    h1.attrs['style'] = style
    h1.string = level.upper()
    try:
        with open(htmlfile, 'w') as fptr:
            fptr.write(str(soup))
    except IOError as e:
        return 'Could not write file. Check permissions and try again.'

def set_crisis_level(level):
    level = level.lower()
    link = "http://brianauron.info/jeff-existential-crisis-level/"
    if level in jeff_crisis_levels.keys() and get_current_level() != level:
        edit_html(level)
        text = "Jeff's existential crisis level has been set to " + level
    elif get_current_level() == level:
        text = "Jeff's existential crisis level is already {0}, ya jerk!".format(level)
    else:
        text = "That is not a valid value for Jeff's existential crisis level, dipshit!"
        end
        text += "\n{0}".format(link)
    return text

def til_sane():
    grad = datetime.date(2016, 5, 31)
    diff = grad - datetime.date.today()
    data = 'Assuming he sticks to the plan, Jeff becomes sane in {0} days.'.format(str(diff.days))
    return data

def jeff_info(data, match):
    verb = match.groups()[0]
    print verb
    if verb in jeff_crisis_levels.keys():
        data['msg'] = [set_crisis_level(verb)]
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
    data['reply'] = 'public'
    return data
