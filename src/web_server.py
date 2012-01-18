# -*- coding: utf-8 -*-

# Copyright (C) 2010 - 2012 Sebastian Ruml <sebastian.ruml@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 1, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import os
import time

from flask import Flask, render_template
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import threading


app = Flask(__name__)

def init_db():
    pass

def connect_db():
    pass

@app.before_request
def before_request():
    # TODO: Make sure that we're connect to the database
    pass

def get_files(directory):
    # TODO: Check if dir exists

    files = os.listdir(directory)

    fileInfos = []
    for file in files:
        filepath = os.path.join(directory, file)

        finfo = FileInfo(file)
        finfo.size = bytes2human(os.path.getsize(filepath))
        finfo.mdate = time.ctime(os.path.getmtime(filepath))
        finfo.isDir = os.path.isdir(filepath)
        fileInfos.append(finfo)

    return fileInfos

@app.route('/')
def index():
    # TODO: Add check for only one share; then redirect to that share
    return render_template('home.html')

@app.route('/shares/')
@app.route('/shares/<int:share_id>/')
def dir(share_id=None):
    # TODO: Get the share path from the config
    if share_id == None:
        share_id = 0

    if share_id is not None and share_id == 0:
        share_path = '/Users/sruml/PythonDrop'
    else:
        share_path = '/Users/sruml/PythonDrop'

    return render_template('dir.html', share_name=share_path, files=get_files(share_path))

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/about')
def about():
    return render_template('about.html')

class WebServer:
    """
    This class creates a tornado based web server.
    """
    def __init__(self):
        app.debug = True
        self.http_server = HTTPServer(WSGIContainer(app))
        self.http_server.listen(4567)

        self.server_thread = threading.Thread(target=self.run)
        self.server_thread.setDaemon(True)
        self.server_thread.start()

    def run(self):
        # Start the IO loop
        IOLoop.instance().start()

####
# Helper classes
####

class FileInfo:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    name = property(get_name, set_name)

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    size = property(get_size, set_size)

    def get_mdate(self):
        return self._mdate

    def set_mdate(self, mdate):
        self._mdate = mdate

    mdate = property(get_mdate, set_mdate)

    def get_isDir(self):
        return self._isDir

    def set_isDir(self, isDir):
        self._isDir = isDir

    isDir = property(get_isDir, set_isDir)

####
# Helper methods
####

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n
