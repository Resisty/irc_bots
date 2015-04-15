def testhelper()
  return 'This message is now different. Loading test helper seems to have worked'
end

$jeff_crisis_levels = {'critical' => {'text' => 'black',
                                     'font' => 'Lucida Console',
                                     'bg' => "\n background-image: url(//brianauron.info/img/critical.gif);\nbackground-size: cover;"},
                      'too damn high' => {'text' => 'red',
                                          'font' => 'Lucida Console',
                                          'bg' => "\n background-image: url(//brianauron.info/img/toodamnhigh.gif);\nbackground-size: cover;"},
                      'cat' => {'text' => 'white',
                                          'font' => 'Arial',
                                          'bg' => "\n background-image: url(//brianauron.info/img/expressive_cat.png);\nbackground-size: cover;"},
                      'can\'t even' => {'text' => 'purple',
                                          'font' => 'Impact',
                                          'bg' => "\n background-image: url(//brianauron.info/img/canteven.gif);\nbackground-size: cover;"},
                      'pants meat' => {'text' => 'pink',
                                          'font' => 'Times New Roman',
                                          'bg' => "\n background-image: url(//brianauron.info/img/pantsmeat.gif);\nbackground-size: cover;"},
                      'under control' => {'text' => 'yellow',
                                          'font' => 'Cursive',
                                          'bg' => "\n background-image: url(//brianauron.info/img/undercontrol.gif);\nbackground-size: cover;"},
                      'linuxpocalypse' => {'text' => 'green',
                                          'font' => 'Impact',
                                          'bg' => "\n background-image: url(//brianauron.info/img/tux.gif);\nbackground-size: cover;"}}
$jeff_crisis_level = 'critical'

def cmds()
 { '[A-Z]{3}' => { 'func' => :manatee_maybe,
                   'i' => false,
                   'help' => 'Any block caps message returns a calming manatee to the agitated nick.'},
   '^panicbutt(|,) enhance$' => { 'func' => :enhance,
                                  'i' => true,
                                  'help' => '"panicbutt, enhance" comma is optional. Panicbutt will enhance the image.'},
   '^fuck (you|off)(|,) panicbutt$' => { 'func' => :fuck_off,
                                         'i' => true,
                                         'help' => '"fuck you/off, panicbutt" comma is optional. Panicbutt is just trying to help, jeez'},
   '^panicbutt what is Jeff$' => { 'func' => :list_jeff,
                                   'i' => true,
                                   'help' => '"panicbutt what is Jeff" will tell you Jeff\'s current existential crisis level. Defaults to critical'},
   'cortana' => { 'func' => :cortana,
                  'i' => true,
                  'help' => 'Any mention of cortana will summon the AI who helped to save the galaxy.'},
   '^panicbutt define windows error message (.*)$' => { 'func' => :windows_error,
                                                        'i' => true,
                                                        'help' => '"panicbutt define windows error message <error string>" panicbutt will try to sort through the incomprehensible mess which is Windows and report back on (hopefully) useful solutions.'},
   '^panicbutt sing [\w]+ happy birthday$' => { 'func' => :happy_birthday,
                                                'i' => true,
                                                'help' => '"panicbutt sing <somebody> happy birthday" panicbutt will serenade somebody with the joyful, celebratory renditions of MC Chris'},
   '^panicbutt tell (.+) to come to Portland$' => { 'func' => :come_to_portland,
                                                    'i' => true,
                                                    'help' => '"panicbutt tell <somebody> to come to Portland" panicbutt will summon the raw, animal magnetism of Hugh Jackman in an attempt to convince somebody to come to Portland. Shhh, just come.'},
   '^panicbutt tell (.+) to come to Seattle$' => { 'func' => :come_to_seattle,
                                                    'i' => true,
                                                    'help' => '"panicbutt tell <somebody> to come to Seattle" panicbutt will display the beautiful scenery and emotion inherent in the Seattle climate in an attempt to convince somebody to come to Seattle.'},
   '^panicbutt roll dice($|.*)' => { 'func' => :roll_dice,
                                     'i' => true,
                                     'help' => '"panicbutt roll dice [number of 6 sided dice]" OR "panicbutt roll dice [set of dice, e.g. 2d8 3d12 1d20] [with <something> modifier +/-<number>]" Panicbutt will try to figure out what the fuck kind of dice you want to roll and roll them. Including the optional modifier string will adjust dice accordingly.'},
   '^panicbutt spin the wheel' => { 'func' => :spin_wheel,
                                    'i' => true,
                                    'help' => '"panicbutt spin the wheel" makes panicbutt spin the Price is Right wheel, not the Wheel of Fortune Wheel \'cuz that\'d be dumb'},
   '^panicbutt butts ([\w-]+) (.*)' => { 'func' => :butts_me,
                                         'i' => true,
                                         'help' => '"panicbutt butts <somebody> <something>" panicbutt will look up <something> (can contain spaces) on giphy for <somebody> (cannot contain spaces, can be "me")'},
   '^panicbutt (.*) Jeff$' => { 'func' => :jeff_stuff,
                                'i' => true,
                                'help' => '"panicbutt <something> Jeff" Does stuff with Jeff\'s existential crisis levels. Options [list,enumerate,print] provide what settings are available for the crisis levels. Options [url,link] provide the web url to view the crisis level in action. Using any of the crisis levels from "list" sets the crisis level accordingly.'},
   '^panicbutt(|,) what is love$' => { 'func' => :haddaway,
                                'i' => true,
                                'help' => '"panicbutt what is love" Panicbutt will spend a night at the Roxbury.'},
   '^panicbutt can bobi spend this money' => { 'func' => :can_bobi_spend,
                                               'i' => true,
                                               'help' => '"panicbutt can bobi spend this money" provides a webpage answering your question'},
   '^panicbutt (-h|--help|help)$' => { 'func' => :panicbutt_help,
                                       'i' => true,
                                       'help' => '"panicbutt -h, panicbutt --help, panicbutt help" print this list of helpful help messages.'},
 }
end

def parse_message(msg)
  replies = []
  cmds.keys().each() do |k|
    if cmds[k]['i']
      reg = Regexp.new(k, Regexp::IGNORECASE)
    else
      reg = Regexp.new k
    end
    if msg =~ reg
      replies.push(send(cmds[k]['func'], msg, reg))
    end
  end
  if replies
    return replies
  else
    return [[nil, nil]]
  end
end

def enhance(msg, reg)
  return "/me types furiously. \"Enhance.\"", false
end

def list_jeff(msg, reg)
  return $jeff_crisis_level, true
end

def fuck_off(msg, reg)
  return ":C", true
end

def cortana(msg, reg)
  return 'http://i0.kym-cdn.com/photos/images/original/000/837/637/7d6.gif', true
end

def windows_error(msg, reg)
  code = msg.scan(reg)
  roll = rand(1000)
  if roll < 150
    return 'Suggested course of action for code %s: install your choice of linux distro' % code[0][0] , true
  elsif roll >= 150 && roll < 160
    return 'Suggested course of action for code %s: Have you tried Dragonfly BSD?' % code[0][0], true
  else
    return 'Suggested course of action for code %s: turn it off and on again' % code[0][0] , true
  end
end

def happy_birthday(msg, reg)
  nick = msg.scan(reg)
  nick = nick[0][0]
  return "Go #{nick}, it\'s your birthday! Go #{nick}, it\'s your birthday! You're one year older, one year wiser, you're a rock 'n roll star, king, czar and kaiser! You're the man of the hour, the VIP! You get the first slice -- of the P-I-E! So blow out your candles and make a wish! Put a smile on -- 'cuz it's your birthday, bitch! Go #{nick}, it's your birthday! Go #{nick}, it's your birthday!", false
end

def come_to_portland(msg, reg)
  who = msg.scan(reg)
  if who[0][0] == 'me'
    return "http://imgur.com/29hMr0h", true
  else
     return who[0][0] + ": http://i.imgur.com/29hMr0h.jpg", false
  end
end

def come_to_seattle(msg, reg)
  who = msg.scan(reg)
  if who[0][0] == 'me'
    return "http://i.imgur.com/Lwo0CTF.gif", true
  else
     return who[0][0] + ": http://i.imgur.com/Lwo0CTF.gif", false
  end
end

def roll_dice(msg, reg)
  n = msg.scan(reg)
  if n[0][0] == ''
    return dice_roll('1').join(', '), true
  else
    return dice_roll(n[0][0]).join(', '), true
  end
end

def jeff_stuff(msg, reg)
  verb = msg.scan(reg)
  verb = verb[0][0]
  keys = $jeff_crisis_levels.keys()
  if keys.any? {|k| k == verb }
    return set_crisis_level(verb), true
  elsif ['list', 'enumerate', 'print'].any? {|word| word == verb}
    return keys.join(", "), true
  elsif ['link', 'url'].any? {|word| word == verb}
    return "http://brianauron.info/jeff-existential-crisis-level/", true
  end
end

def can_bobi_spend(msg, reg)
  return "http://brianauron.info/CanBobiSpendThisMoney", true
end

def haddaway(msg, reg)
  return "Baby don't hurt me! https://www.youtube.com/watch?v=Ktbhw0v186Q", true
end

def panicbutt_help(msg, reg)
  msg = "Panicbutt understands the following messages:\n"
  cmds.keys().each() do |k|
    cmd = cmds[k]['help']
    msg += "#{cmd}\n"
  end
  return msg, true
end

#  if msg == msg.upcase && msg =~ /[A-Z]{3}/ && msg.length > 4
#    return manatee(), true
#  elsif msg =~ /^panicbutt(|,) enhance$/
#    return "/me types furiously. \"Enhance.\"", false
#  elsif msg =~ /^panicbutt what is Jeff$/i
#    return $jeff_crisis_level, true
#  elsif msg =~ /^fuck (you|off)(|,) panicbutt$/
#    return ":C", true
#  elsif msg =~ /cortana/i
#    return 'http://i0.kym-cdn.com/photos/images/original/000/837/637/7d6.gif', true
#  elsif msg =~ /^ panicbutt define windows error message (.*)$/
#    code = msg.scan(/message (.*)/)
#    return 'Suggested course of action for code %s: turn it off and on again' % code[0][0] , true
#  else
#    return nil, nil
#  end
#end

def edit_html(level)
  wordcolor = $jeff_crisis_levels[level]['text']
  bgcolor = $jeff_crisis_levels[level]['bg']
  font = $jeff_crisis_levels[level]['font']

  $fn = '/var/www/html/jeff-existential-crisis-level/index.html'
  text = File.read($fn)
  new_contents = text.gsub(/(body {)(.*)(})/m, "\\1#{bgcolor}\\3")
  File.open($fn, "w") {|file| file.puts new_contents}
  
  $fn = '/var/www/html/jeff-existential-crisis-level/jeff-existential-crisis-level.html'
  text = File.read($fn)
  new_contents = text.gsub(/(font-family: )([\s\w]+)/, "\\1#{font}")
  new_contents = new_contents.gsub(/(color: )([\s\w]+)/, "\\1#{wordcolor}")
  new_contents = new_contents.gsub(/("level">)(.*)(<\/h1>)/, "\\1#{level.upcase}\\3")
  File.open($fn, "w") {|file| file.puts new_contents}
end

def crisis_level()
  return $jeff_crisis_level
end

def set_crisis_level(level)
  level = level.downcase
  link = "http://brianauron.info/jeff-existential-crisis-level/"
  if $jeff_crisis_levels.has_key?(level) && $jeff_crisis_level != level
    $jeff_crisis_level = level
    edit_html(level)
    text = "Jeff's existential crisis level has been set to " + $jeff_crisis_level
  elsif $jeff_crisis_level == level
    text = "Jeff's existential crisis level is already #{level.upcase}, ya jerk!"
  else
    text = "That is not a valid value for Jeff's existential crisis level, dipshit!"
  end
  text = text + "\n#{link}"
  return text
end

def manatee_maybe(msg, reg)
  if msg == msg.upcase && msg.length > 4
    return manatee(), true
  end
end

def manatee()
  num = rand(33) + 1
  url = "http://calmingmanatee.com/img/manatee%s.jpg" % num
  return url
end


def butts_me(msg, reg)
  terms = msg.scan(reg)
  nick = terms[0][0]
  if nick == 'me'
    rep = true
  else
    rep = false
  end
  search = terms[0][1]
  if search == 'manatee'
    return manatee(), rep
  elsif search == 'pants meat'
    return 'http://s3-ec.buzzfed.com/static/2013-12/enhanced/webdr06/2/18/anigif_enhanced-buzz-19264-1386027436-9.gif', rep
  end
  search = search.split(/ /).join('+')
  url = 'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=' + search
  puts url
  uri = URI(url)
  resp = Net::HTTP::get_response(uri)
  result = JSON.parse(resp.body)['data']
  if result.empty?
    return 'That\'s a stupid search!', rep 
  else
    return result['image_original_url'], rep
  end
end

def dice_roll(dicestr)
  puts dicestr
  sets = dicestr.scan(/[0-9]+d[0-9]+/)
  modifier = dicestr.scan(/with .+ modifier ([+-])(\d+)/)
  if !modifier.empty?
    puts "Modifier is NOT empty\n\n"
    if modifier[0][0] == '-'
      mod = "#{modifier[0][0]}#{modifier[0][1]}".to_i
    else
      mod = "#{modifier[0][1]}".to_i
    end
  else
    puts "Modifier is EMPTY\n\n"
    mod = 0
  end
  puts "The MODIFIER is #{mod}"
  dice = []
  if sets.empty?
    num = dicestr.to_i
    (1..num).each do |n|
      dice.push(rand(6) + 1 + mod)
    end
    puts "The empty-setted dice are: #{dice}"
    return dice
  else
    sets.each do |dset|
      numdice, sizedie = dset.split('d')
      dsetstr = "d#{sizedie}s: "
      dsetstr += (1..numdice.to_i).collect{|x| rand(sizedie.to_i) + 1 + mod}.join(', ')
      dice.push(dsetstr)
    end
    puts "The dice are: #{dice}"
    return dice
  end
end


def spin_wheel(msg, reg)
  values = (5..100).step(5)
  return values.to_a.sample, true
end
