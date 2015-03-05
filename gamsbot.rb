require 'cinch'
require 'open-uri'
require 'nokogiri'
require 'cgi'
require 'json'
require 'uri'
require 'net/http'

# This bot connects to urban dictionary and returns the first result
# for a given query, replying with the result directly to the sender

bot = Cinch::Bot.new do
  cnf = YAML::load_file(File.join(__dir__, 'config.yml'))
  configure do |c|
    c.server   = cnf['gamsbot']['server']
    c.nick     = cnf['gamsbot']['nick']
    c.channels = cnf['gamsbot']['channels']
  end

  helpers do
    # This method assumes everything will go ok, it's not the best method
    # of doing this *by far* and is simply a helper method to show how it
    # can be done.. it works!


    def log_it(m, str)
      open('gamsbot.log', 'a') { |f|
        f.puts "gamsbot: #{m.user.nick}: #{str}"
      }
    end

    def manatee()
      num = rand(33) + 1
      url = "calmingmanatee.com/img/manatee%s.jpg" % num
      return url
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
  end

  on :message, /.*/ do |m|
    if m.message =~ /[A-Z]{3}/
      m.reply(manatee(), true)
    end
    open('gamsbot.log', 'a') { |f|
      f.puts "#{m.user.nick}: #{m.message}"
    }
  end

  on :message, /^gamsbot last night the cheese guy came from up north/i do |m, who|
    msg = "It's a cold day for pontooning."
    m.reply(msg, true)
    log_it(m, msg)
  end

  on :message, /^gamsbot tell (.+) to come to Portland/i do |m, who|
    if who == "me"
      msg = "http://imgur.com/29hMr0h"
      m.reply(msg, true)
      log_it(m, msg)
    else
      msg = "@" + who + ": http://i.imgur.com/29hMr0h.jpg"
      m.reply(msg, false)
      log_it(m, msg)
    end
  end

  on :message, /^gamsbot image (\w+) (.*)/i do |m, who, terms|
    if who == 'me'
      msg = butts_me(terms)
      m.reply(msg, true)
      log_it(m, msg)
    else
      msg = '@' + who + ': ' + butts_me(terms)
      m.reply(msg, false)
      log_it(m, msg)
    end
  end
end

bot.start

# injekt> !urban cinch
# MrCinch> injekt: describing an action that's extremely easy.
