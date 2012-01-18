# Copyright (C) 2010 - 2012 Sebastian Ruml <sebastian.ruml@gmail.com>
#
# This file is part of the PythonDrop project.
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
import threading
import SocketServer
from datetime import date

import log
import globals

PythonDrop = None

class ApiRequestHandler(SocketServer.StreamRequestHandler):
    """
    The request handler for our API server.
    """

    help_message = "Available commands\n\r"
    help_message += "  -> quit:\t Close connection\n\r"
    help_message += "  -> exit:\t Exit PythonDrop\n\r"
    help_message += "  -> version:\t Prints the version\n\r"
    help_message += "  -> about:\t Prints a short description\n\r"

    available_options = "Available options\n\r"
    available_options += "  -> syncinterval:\t Duration for the interval for synchronization\n\r"

    about_message = "\n\r"

    def __init__(self, request, client_address, server):
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)

    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        self._logger = log.Logger()
        self._logger.info("Client connected")
        self._config = globals.Globals().config

    def handle(self):
        client_info = "Client connected from %s\n\r" % self.client_address[0]
        #self.wfile.write(client_info)
        welcome_message = "Welcome to PythonDrop (%s). Type \"help\" for a list with all available commands.\n\r" % str(date.today())
        #self.wfile.write(welcome_message)
        #self.wfile.write_line_break()

        command = self.rfile.readline().strip().lower()
        while command != None:
            if command == 'quit':
                # Quits the connection
                self.wfile.write("Closing connection. Hope to see you again!\n\r")
                break
            elif command == 'stop':
                # Stops watching the repository
                self.wfile.write("Stop watching...")
                PythonDrop.stop()
            elif command == 'start':
                # Starts watching the repository
                self.wfile.write("Start watching...")
                PythonDrop.start()
            elif command == 'help':
                # Shows all available commands and a help message
                self.wfile.write(self.help_message)
            elif command == 'exit':
                # Exits the daemon
                sys.exit(2)
            elif command == 'update_interval':
                # Sets the update interval
                # 1. Stop syncing
                # 2. Update sync interval (config + fswatcher)
                # 3. Resume syncing
                # TODO: Move it to the set section
                print "Update interval changed"
            elif command == 'about':
                pass
            elif command == 'version':
                self.wfile.write(globals.Globals().version + "\n\r")
            elif command.startswith('get'):
                parts = command.split(' ')
                if len(parts) == 1:
                    # Return a list with all available option
                    self.wfile.write(self.available_options)
                elif len(parts) == 2:
                    option = parts[1]
                    if option == "syncinterval":
                        value = self._config.get_option('syncInterval', 'general')
                        self.wfile.write(str(value) + "\n\r")
                    elif option == "syncfolder":
                        value = self._config.get_option('syncFolder', 'general')
                        self.wfile.write(str(value) + "\n\r")
                    elif option == "remoteuser":
                        value = self._config.get_option('remoteUser', 'repository')
                        self.wfile.write(str(value) + "\n\r")
                    elif option == "remotehost":
                        value = self._config.get_option('remoteHost', 'repository')
                        self.wfile.write(str(value) + "\n\r")
                    elif option == "remoterep":
                        value = self._config.get_option('remoteRepositoryPath', 'repository')
                        self.wfile.write(str(value) + "\n\r")
            elif command.startswith('set'):
                # Sets an option
                pass
            else:
                self.wfile.write("Invalid command\n\r")

            command = self.rfile.readline().strip().lower()

    def finish(self):
        SocketServer.StreamRequestHandler.finish(self)
        self._logger.info("Client disconnected")

    def print_help(self):
        self.wfile.write(self.help_message)


class ApiServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class implements the API server.
    """

    def __init__(self, pythondrop, host, port):
        global PythonDrop
        PythonDrop = pythondrop

        self._logger = log.Logger()

        self.server_address = (host, port)
        SocketServer.TCPServer.__init__(self, self.server_address, ApiRequestHandler)

        # Start a thread with the server -- that thread will start one
        # more thread for each request
        server_thread = threading.Thread(target=self.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.setDaemon(True)
        server_thread.start()

        self._logger.info("API server listening on " + host + ", " + str(port))
