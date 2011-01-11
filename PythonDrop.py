#!/usr/bin/env python

# Copyright (C) 2010 Sebastian Ruml <sebastian.ruml@gmail.com>
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

import os
import sys
import platform
import subprocess

from src import pythondrop
from src import globals as gl

__appName__ = 'PythonDrop'
__version__ = '0.1.0'


# Check that at least Python 2.5 is running
if sys.version_info < (2, 5):
    print _('Python version must be at least 2.5.')
    sys.exit(1)
    
if platform.system() is not "Windows":
    print _('Currently only Windows is supported')
    sys.exit(1)
    
    
def main():
    """
    Everything dispatches from this main function
    """
    # Start the PythonDrop daemon
    #pythondrop.PythonDrop()
    subprocess.Popen("python src/pythondrop.py")
    
    # Start the PythonDrop GUI
    subprocess.Popen("python src/gui/pythondrop_ui.py")


if __name__ == '__main__':
	try:
		main()
	except SystemExit:
		raise
	except: # BaseException doesn't exist in python2.4
		import traceback
		traceback.print_exc()
