# WSGI Files related to Jeff's Existential Crisis Level

Not really related to an IRC bot per se, but they're part of this project now.

Location should be /var/www/html/

Make sure to add WSGI configuration to apache:
```
  WSGIDaemonProcess jeff-level group=characterscraper threads=1 user=characterscraper
  WSGIProcessGroup jeff-level
  WSGIScriptAlias /jeff-level "/var/www/html/flaskjeff.wsgi"
```
