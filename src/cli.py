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
from optparse import OptionParser

from app_manager import AppManager
from configuration import Configuration

pythondrop_app = None

class Cli():
    def __init__(self, args, options):
        self._args = args
        self._options = options

        self._usage = "usage: %prog start|stop|restart"

        self._app = None
        self._config = Configuration()

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

    def start(self):
        app = AppManager(self.pid_file, pidfile=self._options.debugmode)
        if self._options.debugmode:
            app.run()
        else:
            app.start()

    def stop(self):
        pass

    def restart(self):
        self.stop()
        self.start()

    def create(self):
        pass

    def status(self):
        pass

    def config(self):
        pass

    def help(self):
        pass

    def running(self):
        pass

    def stopped(self):
        pass

    def pid_file(self):
        return "/tmp/pythondrop.pid"
