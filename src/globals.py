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


globals = None

class _Globals:
    def __init__(self):
        self.appName = None
        self.version = None
        self.pythondrop = None
        self.baseDir = None
        self.confDir = None
        self.cfgFile = None
        self.cfgDb = None
        self.config = None
        self.argv = None

        # Default configuration
        self.DEFAULT_CONFIG = """\
        [general]
        logLevel = 'DEBUG'
        syncFolder = ''
        syncInterval = 5
        tcpListenIp = '127.0.0.1'
        tcpListenPort = 12444
        enableGui = True

        [repository]
        remoteUser = ''
        remoteHost = ''
        remoteRepositoryPath = ''"""

def Globals():
    global globals
    if not globals:
        globals = _Globals()
    return globals
