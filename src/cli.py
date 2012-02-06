# -*- coding: utf-8 -*-

# Copyright (C) 2012 Sebastian Ruml <sebastian.ruml@gmail.com>
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

import sys

from app_manager import AppManager
import globals

pythondrop_app = None

class Cli():
    def __init__(self, args, options):
        self._args = args
        self._options = options

        self._usage = "usage: %prog start|stop|restart"

        self._app = AppManager(self.pid_file(), debug=self._options.debugmode)
        self._config = self._app._config
        self._globs = globals.Globals()

        self.parseArgs()

    def parseArgs(self):
        # Check for the correct numbers of arguments
        if len(self._args) != 1:
            print self._usage
            sys.exit(2)

        if self._args[0] == 'start':
            self.start()
        elif self._args[0] == 'stop':
            self.stop()
        elif self._args[0] == 'restart':
            self.restart()
        elif self._args[0] == 'create':
            self.create()
        elif self._args[0] == 'status':
            self.status()
        elif self._args[0] == 'config':
            self.config()
        elif self.args[0] == 'factoryreset':
            pass
        else:
            print "Unknown command"
            print self._usage
            sys.exit(2)

    def start(self):
        print "Starting PythonDrop..."
        if self.stopped() and not self._options.debugmode:
            self._app.start()
        elif self.stopped() and self._options.debugmode:
            # Start in debug mode
            self._app.run()
        else:
            print "PythonDrop is already running, please use restart"

    def stop(self):
        print "Stopping PythonDrop..."
        if self.running:
            self._app.stop()
            print "PythonDrop stopped"
        else:
            print "PythonDrop is not running"

    def restart(self):
        self.stop()
        self.start()

    def create(self):
        if len(self._args) < 4:
            print "Error"

    def status(self):
        print "PythonDrop v" + self._globs.version
        print "Running: True" if self.running() else "Running: False"
        print "Shares:"
        print "\n".join("  - " + share.sync_folder for share in self._config.get_shares())

    def config(self):
        if len(self._args) == 1:
            # TODO: Print configuration
            print "Configuration:"
            print "  - Log Level: " + self._config.logLevel
            print "  - API Listen IP: " + self._config.tcpListenIp
            print "  - API Listen Port: " + str(self._config.tcpListenPort)
            print "  - Web Server Enabled: " + str(self._config.enableWebServer)
            print "  - Web Server Listen IP: " + self._config.webServerListenIp
            print "  - Web Server Listen Port: " + str(self._config.webServerListenPort)
            print "  - Systray Enabled: " + str(self._config.enableSystray)

    def help(self):
        pass

    def running(self):
        return self._app.running()

    def stopped(self):
        return self._app.stopped()

    def pid_file(self):
        return "/tmp/pythondrop.pid"
