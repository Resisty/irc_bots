require 'cinch'
require 'open-uri'
require 'nokogiri'
require 'cgi'
require 'json'
require 'uri'
require 'net/http'
require 'yaml'

# This bot connects to urban dictionary and returns the first result
# for a given query, replying with the result directly to the sender

bot = Cinch::Bot.new do
  cnf = YAML::load_file(File.join(__dir__, 'config.yml'))
  configure do |c|
    c.server   = cnf['panicbutt']['server']
    c.nick     = cnf['panicbutt']['nick']
    c.channels = cnf['panicbugg']['channels']
  end

  helpers do
    # This method assumes everything will go ok, it's not the best method
    # of doing this *by far* and is simply a helper method to show how it
    # can be done.. it works!

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

    def butts_me(search)
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

    def dice_roll(numdice)
      dice = []
      num = numdice.to_i
      (1..num).each do |n|
        dice.push(rand(6) + 1)
      end
      return dice
    end

    def spin_wheel()
      values = (5..100).step(5)
      return values.to_a.sample
    end
  end


  on :message, /^panicbutt tell (.+) to come to Portland/i do |m, who|
    if who == "me"
      m.reply("http://imgur.com/29hMr0h", true)
    else
      m.reply("@" + who + ": http://i.imgur.com/29hMr0h.jpg", false)
    end
  end

  on :message, /^panicbutt roll dice($|\s*[0-9]*)/i do |m, n|
    if n == ''
      puts 'n was empty!'
      m.reply(dice_roll('1').join(', '), true)
    else
      puts 'n was NOT empty!'
      m.reply(dice_roll(n).join(', '), true)
    end
  end

  on :message, /^panicbutt spin the wheel/i do |m, n|
    m.reply(spin_wheel(), true)
  end

  on :message, /^panicbutt pants meat (.*)/i do |m, terms|
    if terms == 'me'
      m.reply('http://s3-ec.buzzfed.com/static/2013-12/enhanced/webdr06/2/18/anigif_enhanced-buzz-19264-1386027436-9.gif', true)
    elsif terms.downcase == 'jeff'
      def do_nothing
        # let it happen further down /^panicbutt ((.*) Jeff|Jeff is at (.*))/
      end
    else
      m.reply('@' + terms + ': http://s3-ec.buzzfed.com/static/2013-12/enhanced/webdr06/2/18/anigif_enhanced-buzz-19264-1386027436-9.gif', false)
    end
  end

  on :message, /^panicbutt butts ([\w-]+) (.*)/i do |m, user, terms|
    if user == 'me'
      m.reply(butts_me(terms), true)
    else
      m.reply('@' + user + ": " + butts_me(terms), false)
    end
  end

  on :message, /^panicbutt ((.*) Jeff|Jeff is at (.*))/i do |m, outer, inner|
    if inner == 'list' or inner == 'what are'
      @keys = $jeff_crisis_levels.keys()
      m.reply(@keys.join(", "), true)
    else
      m.reply(set_crisis_level(inner), true)
    end
  end

  on :message, /^panicbutt (|what is )*Jeff's existential crisis level/i do |m|
    m.reply(crisis_level(), true)
  end

  on :message, /^panicbutt Jeff's existential crisis level is (.*)/i do |m, term|
    m.reply(set_crisis_level(term), true)
  end
end

bot.start

# injekt> !urban cinch
# MrCinch> injekt: describing an action that's extremely easy.
