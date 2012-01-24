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

from fswatcher import FSWatcher
from api_server import ApiServer
from config import Config
from configuration import Configuration
from gui import pythondrop_ui
from daemon import Daemon
from web_server import WebServer
import globals
import log

import os


__appName__ = 'PythonDrop'
__version__ = '0.2.0'


# Initialize some global variables
globalVars = globals.Globals()
globalVars.version = __version__
globalVars.baseDir = os.path.dirname(os.path.realpath(__file__))
globalVars.confDir = globalVars.baseDir
globalVars.confDir = os.path.join(os.path.expanduser('~'), '.' + __appName__)
globalVars.cfgFile = os.path.join(globalVars.confDir, 'config.ini')
globalVars.cfgDb = os.path.join(globalVars.confDir, 'config.db')


class AppManager(Daemon):
    def __init__(self, pidfile):
        Daemon.__init__(self, pidfile)

        self._systray = None

        # Get the globals
        self._globals = globals.Globals()

        # Create the logger
        self._logger = log.Logger()

		# Load settings
        self._configOld = Config(self._globals.cfgFile, self._globals.DEFAULT_CONFIG)
        #self._globals.config = self._config

        self._config = Configuration()
        self._globals.config = self._config

        # Set the log level
        self._logger.set_level(self._config.logLevel)

        self._logger.info("Starting PythonDrop v" + self._globals.version + "...")

		# Create and start the API server
        self._api_server = ApiServer(self, self._config.tcpListenIp, self._config.tcpListenPort)

        # Start the web server
        self.web_server = WebServer()

        # TODO: Add support for more than one share!

        # Check if the systray should be shown
        if self._config.enableSystray:
            self._logger.debug("Creating systray...")
            self._systray = pythondrop_ui.Systray(self._globals)

		# Create the file watcher
        self._fswatcher = FSWatcher(self._configOld)

    def run(self):
		# Start watching and syncing files
        self._fswatcher.watch()

	def start(self):
		"""
		Starts watching the repository.
		"""
		self._fswatcher.start()

	def stop(self):
		"""
		Stops watching the repository.
		"""
		self._fswatcher.stop()

    def reastart(self):
        pass

    def pause(self):
        pass

    def exit(self):
        if self._config.get_option('enableGui', 'general'):
            self._systray.exit()


if __name__ == '__main__':
	try:
		PythonDrop()
	except SystemExit:
		raise
	except: # BaseException doesn't exist in python2.4
		import traceback
		traceback.print_exc()
