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

def manatee()
  num = rand(33) + 1
  url = "http://calmingmanatee.com/img/manatee%s.jpg" % num
  return url
end


def butts_me(search)
  if search == 'manatee'
    return manatee()
  end
  search = search.split(/ /).join('+')
  url = 'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=' + search
  puts url
  uri = URI(url)
  resp = Net::HTTP::get_response(uri)
  result = JSON.parse(resp.body)['data']
  if result.empty?
    return 'That\'s a stupid search!' 
  else
    return result['image_original_url']
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
  puts "The modifier is #{mod}"
  dice = []
  if sets.empty?
    num = dicestr.to_i
    (1..num).each do |n|
      dice.push(rand(6) + 1 + mod)
    end
    return dice
  else
    sets.each do |dset|
      numdice, sizedie = dset.split('d')
      dsetstr = "d#{sizedie}s: "
      dsetstr += (1..numdice.to_i).collect{|x| rand(sizedie.to_i) + 1 + mod}.join(', ')
      dice.push(dsetstr)
    end
    return dice
  end
end


def spin_wheel()
  values = (5..100).step(5)
  return values.to_a.sample
end
