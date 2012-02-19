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

globals = None

class _Globals:
    def __init__(self):
        self.appName = 'PythonDrop'
        self.version = '0.2.0'
        self.pythondrop = None
        self.baseDir = None
        self.confDir = os.path.join(os.path.expanduser('~'), '.' + self.appName)
        self.cfgFile = os.path.join(self.confDir, 'config.ini')
        self.cfgDb = os.path.join(self.confDir, 'config.db')
        self.logFile = os.path.join(self.confDir, 'pythondrop.log')
        self.config = None
        self.argv = None

        self.DEFAULT_CONFIG = ""

def Globals():
    global globals
    if not globals:
        globals = _Globals()
    return globals
