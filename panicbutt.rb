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
  cnf = YAML.load_file('config.yaml')
  configure do |c|
    c.server   = cnf['panicbutt']['server']
    c.nick     = cnf['panicbutt']['nick']
    c.channels = cnf['panicbutt']['channels']
  end

  helpers do
    # This method assumes everything will go ok, it's not the best method
    # of doing this *by far* and is simply a helper method to show how it
    # can be done.. it works!

    load 'panicbutt_helpers.rb'
    def reload()
      load 'panicbutt_helpers.rb'
    end
  end

  on :message, /.*/ do |m|
    msg = m.message
    msg, rep = parse_message(msg)
    if msg
      m.reply(msg, rep)
    end
  end

  on :message, /^panicbutt tell (.+) to come to Portland/i do |m, who|
    if who == "me"
      m.reply("http://imgur.com/29hMr0h", true)
    else
      m.reply("@" + who + ": http://i.imgur.com/29hMr0h.jpg", false)
    end
  end

  on :message, /^panicbutt roll dice($|.*)/i do |m, n|
    if n == ''
      m.reply(dice_roll('1').join(', '), true)
    else
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

  on :message, /^panicbutt (.*) Jeff$/i do |m, inner|
    keys = $jeff_crisis_levels.keys()
    if keys.any? {|k| k == inner }
      m.reply(set_crisis_level(inner), true)
    elsif ['list', 'enumerate', 'print'].any? {|word| word == inner}
      m.reply(keys.join(", "), true)
    end
  end

  on :message, /^panicbutt (|what is )*Jeff's existential crisis level/i do |m|
    m.reply(crisis_level(), true)
  end

  on :message, /^panicbutt reload$/ do |m|
    m.reply(reload(), true)
  end
  on :message, /^panicbutt testhelper method$/ do |m|
    m.reply(testhelper(), true)
  end

  on :message, /^panicbutt Jeff's existential crisis level is (.*)/i do |m, term|
    m.reply(set_crisis_level(term), true)
  end
end

bot.start

# injekt> !urban cinch
# MrCinch> injekt: describing an action that's extremely easy.
