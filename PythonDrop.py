#!/usr/bin/env python

# Copyright (C) 2010 - 2012 Sebastian Ruml <sebastian.ruml@gmail.com>
#
# This file is part of the PythonDrop project
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
import platform

from src import app_manager
from src import config
from optparse import OptionParser

__appName__ = 'PythonDrop'
__version__ = '0.2.0'

# Check that at least Python 2.5 is running
if sys.version_info < (2, 5):
    print ('Python version must be at least 2.5.')
    sys.exit(1)
if platform.system() != "Windows" and platform.system() != "Darwin":
    print ('Currently only Windows and Mac OS X are supported!')
    sys.exit(1)

# find out if they are asking for help
HELP = False
for val in sys.argv:
    if val == '-h' or val == '--help': HELP = True

def main():
    """
    Everything dispatches from this main function.
    """
    usage = "usage: %prog start|stop|restart"

    # Parse the command line
    (options, args) = config.clParser(OptionParser(usage=usage, version=__version__)).parseArgs(HELP)
    if HELP:
        sys.exit(0)

    # Check for the correct numbers of arguments
    if len(args) != 1:
        print "usage: PythonDrop.py start|stop|restart"
        sys.exit(2)

    daemon = app_manager.AppManager("/tmp/pythondrop.pid")
    # Parse args
    if args[0] == "start":
        if options.debugmode:
            daemon.run()
        else:
            daemon.start()
    elif args[0] == "stop":
        daemon.stop()
    elif args[0] == "restart":
        daemon.restart()
    else:
        print "Unknown command"
        print "usage: PythonDrop.py start|stop|restart"

    sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
    except: # BaseException doesn't exist in python 2.4
        import traceback
        traceback.print_exc()
