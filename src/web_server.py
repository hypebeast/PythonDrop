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

from configuration import Configuration

# Our Flask app
app = Flask(__name__)

# Configuration
configuration = None

def init_db():
    pass

def connect_db():
    # Connect to the database
    pass

@app.before_request
def before_request():
    # TODO: Make sure that we're connect to the database
    pass

@app.route('/')
def index():
    # TODO: Add check for only one share; then redirect to that share
    return render_template('home.html')

@app.route('/shares/')
@app.route('/shares/<int:share_id>/')
@app.route('/shares/<int:share_id>/<path:dir>/')
def dir(share_id=None, dir=None):
    global configuration
    # TODO: Get the share path from the config
    shares = configuration.shares

    if share_id == None:
        share_id = 1

    share = next((share for share in shares if str(share.id) == share_id), None)

    if share is not None:
        share_path = share.sync_folder
    else:
        pass

    # Get the active directory and build the path parts for the breadcrumb
    dirs = []
    if dir is not None:
        dir_path = os.path.join(share_path, dir)
        path_parts = dir.split('/')
        first = True
        for p in path_parts:
            dirInfo = DirInfo(p)
            if first:
                dirInfo.url = "shares/" + str(share_id) + '/' + p
                parent_url = dirInfo.url
                first = False
            else:
                dirInfo.url = parent_url + '/' + p
                parent_url = dirInfo.url

            dirs.append(dirInfo)
    else:
        dir_path = share_path
        path_parts = None

    # Get all files in the given directory
    files = get_files(dir_path)
    if files is not None:
        for file in files:
            if dir is not None:
                file.url = "shares/" + str(share_id) + '/' + dir + '/' + file.name
            else:
                file.url = "shares/" + str(share_id) + '/' + file.name

    return render_template('dir.html',
            share_name=share_path,
            files=sort_files(files),
            path_parts=dirs)

@app.route('/shares/new')
def add_share():
    pass

@app.route('/settings')
def settings():
    global configuration
    settings = configuration.app_settings()
    return render_template('settings.html', settings=settings)

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
        # Create the config
        global configuration
        configuration = Configuration()

        # Start the IO loop
        IOLoop.instance().start()

####
# Helper classes
####

class DirInfo:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    name = property(get_name, set_name)

    def get_path(self):
        return self._path

    def set_path(self, path):
        self._path = path

    path = property(get_path, set_path)

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = url

    url = property(get_url, set_url)


class FileInfo:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    name = property(get_name, set_name)

    def get_path(self):
        return self._path

    def set_path(self, path):
        self._path = path

    path = property(get_path, set_path)

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = url

    url = property(get_url, set_url)

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

def get_files(directory):
    # TODO: Check if dir exists

    # Find all files in the given directory
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

def sort_files(files):
    directories = []
    filenames = []
    for file in files:
        if file.isDir:
            directories.append(file)
        else:
            filenames.append(file)

    directories.sort(key=lambda dir: unicode.lower(unicode(dir.name)))
    filenames.sort(key=lambda file: unicode.lower(unicode(file.name)))
    directories.extend(filenames)
    return directories

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

def date2human(date):
    """
    Converts the given date to nice readable format.
    """
    pass
