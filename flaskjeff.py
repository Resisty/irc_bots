#!/usr/bin/env python
from bs4 import BeautifulSoup
from flask import Flask, flash, redirect, render_template, request, url_for
from flask import session, Response, abort, jsonify, make_response, current_app
from flask import send_from_directory
from functools import wraps, update_wrapper
from datetime import datetime, timedelta
import urllib2, socket, struct, json, os
from pprint import pprint
import traceback
import jeff
import playhouse.shortcuts


static_root = os.path.abspath(os.path.curdir)
# Create a thread to execute function func
# with arguments args. Args must be a list
def spinoff_thread(func,args,kwargs=None):
    thr = threading.Thread(target=func,args=args,kwargs=kwargs)
    thr.daemon = True
    thr.start()

app = Flask(__name__, static_url_path=os.path.abspath(os.path.curdir))
app.secret_key = os.urandom(32)

@app.errorhandler(404)
def page_not_found(e):
    try:
        img_dir = os.path.join(static_root, 'img')
    except Exception as e:
        return ('Well met!'), 404
    return send_from_directory(img_dir, 'wellmet.png'), 404

@app.errorhandler(500)
def page_not_found_500(e):
    try:
        img_dir = os.path.join(static_root, 'img')
    except Exception as e:
        return ('Well met!'), 500
    return send_from_directory(img_dir, 'wellmet.png'), 500

@app.route('/', methods=['GET'])
def jeff_level():
    jeff.psql_db.connect()
    recent = (jeff.Level
              .select()
              .join(jeff.JeffCrisis,
                    on = (jeff.Level.name == jeff.JeffCrisis.level))
              .order_by(jeff.JeffCrisis.id.desc())
              .get())
    info = playhouse.shortcuts.model_to_dict(recent)
    info['level'] = info['name'].upper()
    return jsonify(info)

if __name__ == '__main__':
    app.run(host='brianauron.info', port=8080, debug = True)
