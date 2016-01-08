#!/usr/bin/python
# =======================================
#
#  File Name: mapping.py
#
#  Purpose: Maps regexes and help info to functions from imported modules.
#
#  Creation Date: 01-05-2015
#
#  Last Modified: Fri 01 May 2015 0120:39 PM CDT
#
#  Created By: Brian Auron
#
# ========================================

import jeff
reload(jeff)
import chatfuncs
reload(chatfuncs)
import snorts
reload(snorts)

def panicbutt_help(data, match):
    newdata = data
    help_lst = [j['help'] for i, j in mapping]
    newdata['msg'] = help_lst
    newdata['reply'] = 'private'
    return newdata

mapping =  [  ('^panicbutt ([\s\w\']+) Jeff($| becomes sane| graduates)',
                 { 'func': jeff.jeff_info,
                   'i': True,
                   'help': '"panicbutt [question] Jeff [state of being]" Access panicbutt\'s wealth of knowledge and power on Jeff. Options: [list,enumerate,print], [url,link], [level from "list"], [how long, when will <requires [state of being]>].'}),

              ('[A-Z]{3}',
                 { 'func': chatfuncs.manatee_maybe,
                   'i': False,
                   'help': 'Any block caps message returns a calming manatee to the agitated nick.'}),

             ('^panicbutt(|,) enhance$',
                 { 'func': chatfuncs.enhance,
                   'i': True,
                   'help': '"panicbutt, enhance" comma is optional. Panicbutt will enhance the image.'}),

             ('^fuck (you|off)(|,) panicbutt$',
                 { 'func': chatfuncs.fuck_off,
                   'i': True,
                   'help': '"fuck you/off, panicbutt" comma is optional.  Panicbutt is just trying to help, jeez'}),

             ('Cortana',
                 { 'func': chatfuncs.cortana,
                   'i': False,
                   'help': 'Any mention of "Cortana" will summon the AI who helped to save the galaxy.'}),

             ('^panicbutt define windows error message (.*)$',
                 { 'func': chatfuncs.windows_error,
                   'i': True,
                   'help': '"panicbutt define windows error message <error string>" panicbutt will try to sort through the incomprehensible mess which is Windows and report back on (hopefully) useful solutions.'}),

             ('^panicbutt sing [\w]+ happy birthday$',
                 { 'func': chatfuncs.happy_birthday,
                   'i': True,
                   'help': '"panicbutt sing <somebody> happy birthday" panicbutt will serenade somebody with the joyful, celebratory renditions of MC Chris'}),

             ('^panicbutt tell (.+) to come to Portland$',
                 { 'func': chatfuncs.come_to_portland,
                   'i': True,
                   'help': '"panicbutt tell <somebody> to come to Portland" panicbutt will summon the raw, animal magnetism of Hugh Jackman in an attempt to convince somebody to come to Portland. Shhh, just come.'}),

             ('^panicbutt tell (.+) to come to Seattle$',
                 { 'func': chatfuncs.come_to_seattle,
                   'i': True,
                   'help': '"panicbutt tell <somebody> to come to Seattle" panicbutt will display the beautiful scenery and emotion inherent in the Seattle climate in an attempt to convince somebody to come to Seattle.'}),

             ('^panicbutt tell (.+) to come to Cleveland$',
                 { 'func': chatfuncs.come_to_cleveland,
                   'i': True,
                   'help': '"panicbutt tell <somebody> to come to Cleveland" panicbutt will display the beautiful scenery and emotion inherent in the Cleveland climate in an attempt to convince somebody to come to Cleveland.'}),

             ('^panicbutt roll dice($| ((\s*[\d]+d[\d]+)+)($| with .* modifier(|s) ((\s*[\+-]\d+)+)))',
                 { 'func': chatfuncs.roll_dice,
                   'i': True,
                   'help': '"panicbutt roll dice [number of 6 sided dice]" OR "panicbutt roll dice [set of dice, e.g. 2d8 3d12 1d20] [with <something> modifier +/-<number>]" Panicbutt will try to figure out what the fuck kind of dice you want to roll and roll them. Including the optional modifier string will adjust dice accordingly.'}),

             ('^panicbutt spin the wheel',
                 { 'func': chatfuncs.spin_wheel,
                   'i': True,
                   'help': '"panicbutt spin the wheel" makes panicbutt spin the Price is Right wheel, not the Wheel of Fortune Wheel \'cuz that\'d be dumb'}),

             ('^panicbutt butts ([\w-]+) (.*)',
                 { 'func': chatfuncs.butts_me,
                   'i': True,
                   'help': '"panicbutt butts <somebody> <something>" panicbutt will look up <something> (can contain spaces) on giphy for <somebody> (cannot contain spaces, can be "me")'}),

             ('^panicbutt urban ([\w-]+) ([\w\s-]+)($| #\d+)',
                 { 'func': chatfuncs.urban,
                   'i': True,
                   'help': '"panicbutt urban <somebody> <something> [#<definition number>]" panicbutt will look up <something> (can contain spaces) on Urban Dictionary for <somebody> (cannot contain spaces, can be "me"). If provided, definition number will look up the Nth definition, if it exists.'}),

             ('^panicbutt(|,) what is love$',
                 { 'func': chatfuncs.haddaway,
                   'i': True,
                   'help': '"panicbutt what is love" Panicbutt will spend a night at the Roxbury.'}),

             ('^panicbutt can (.*) spend (this|that|the) money',
                 { 'func': chatfuncs.can_bobi_spend,
                   'i': True,
                   'help': '"panicbutt can bobi spend this money" provides a webpage answering your question'}),

             ('fixit',
                  { 'func': chatfuncs.fixit,
                    'i': True,
                    'help': 'Any mention of fixit will link you to the fixit video.'}),

              ('(coffee|good sludge|fresh pot!)',
                  { 'func': chatfuncs.good_sludge,
                    'i': True,
                    'help': 'Any mention of coffee (the good sludge) will cause panicbutt to regale you with a true fact regarding its obsession with coffee.'}),

              ('whelps',
                  { 'func': chatfuncs.whelps,
                    'i': True,
                    'help': 'Onyxia Wipes have been known to occur, given certain stimuli.'}),

              ('^panicbutt snort ([\w-]+)',
                  { 'func': snorts.snort_me,
                    'i': True,
                    'help': 'panicbutt snort <nick> increment nick\'s snort counter for the day'}),

              ('^panicbutt show snorts',
                  { 'func': snorts.show_snorts,
                    'i': True,
                    'help': 'panicbutt show snorts list snorts for the day'}),

              ('^panicbutt (-h|--help|help|halp)$',
                  { 'func': panicbutt_help,
                    'i': True,
                    'help': '"panicbutt -h, panicbutt --help, panicbutt h[ae]lp" print this list of helpful help messages.'}),

              ('this is fine',
                  { 'func': chatfuncs.this_is_fine,
                    'i': True,
                    'help': 'Asserting that anything is fine will force panicbutt to demonstrate that everything is not necessarily fine.'}),

              ('^panicbutt (\w+)(\+\+|--)$',
                  { 'func': snorts.count_update,
                    'i': True,
                    'help': '"<variable>++, <variable>--" increment or decrement the variable'}),

              ('^panicbutt delete (\w+)$',
                  { 'func': snorts.count_delete,
                    'i': True,
                    'help': 'Delete the variable (only works if variable\'s count is 0.'}),

              ('^panicbutt:? print (\w+)$',
                  { 'func': snorts.count_get,
                    'i': True,
                    'help': '"panicbutt print <variable>" print the variable'}),

              ('^panicbutt list counts$',
                  { 'func': snorts.count_list,
                    'i': True,
                    'help': '"panicbutt list counts" will show all keys being counted in the database'}),

              ('^(["\'\*]*)([a-zA-Z]+)ING(["\'\*]*)( ME( PANICBUTT)?)?$',
                  { 'func': chatfuncs.ping,
                    'i': True,
                    'help': '"PING" will make tell panicbutt you\'re feeling solipsistic and come to the rescue with a reassuring message.'}),

              ('^.*$',
                  { 'func': chatfuncs.annoy_jeff,
                    'i': True,
                    'help': 'Every message has a 1 in 10 chance to pester Jeff about his employment/life/happiness.'}),

              ('^.*$',
                  { 'func': chatfuncs.seasonal,
                    'i': True,
                    'help': 'Gobble gobble!'}),
]
