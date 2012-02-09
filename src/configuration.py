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

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import Sequence
from sqlalchemy.orm import scoped_session, sessionmaker

import globals

Base = declarative_base()

class ConfigurationError(Exception):
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class Configuration:
    """
    Configuration
    """
    def __init__(self):
        self._globals = globals.Globals()

        if not os.path.exists(self._globals.confDir):
            try:
                os.makedirs(self._globals.confDir)
            except OSError, error:
                raise ConfigurationError(error)

        # Open the database
        self._engine = create_engine('sqlite:///' + self._globals.cfgDb, convert_unicode=True)
        Session = scoped_session(sessionmaker(autocommit=False,
                                                    autoflush=False,
                                                    bind=self._engine))
        self._dbSession = Session()

        if not os.path.exists(self._globals.cfgDb):
            Base.metadata.create_all(self._engine)
            self.create_default_config()
            self.add_test_share()

    class Share(Base):
        __tablename__ = 'shares'

        id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
        polling_intervall = Column(Integer)
        sync_folder = Column(String(250))
        remote_host = Column(String(250))
        remote_path = Column(String(250))
        remote_user = Column(String(100))

        def __init__(self, sync_folder, remote_host, remote_path, remote_user):
            self.sync_folder = sync_folder
            self.remote_host = remote_host
            self.remote_path = remote_path
            self.remote_user = remote_user
            self.polling_intervall = 10


    class Settings(Base):
        __tablename__ = 'settings'

        id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
        logLevel = Column(String(50))
        enableSystray = Column(Boolean())
        tcpListenIp = Column(String(50))
        tcpListenPort = Column(Integer)
        enableWebServer = Column(Boolean())
        webServerListenIp = Column(String(50))
        webServerListenPort = Column(Integer)

        def __init__(self):
            pass

    def create_default_config(self):
        settings = self.Settings()
        settings.logLevel = "INFO"
        settings.enableSystray = False
        settings.tcpListenIp = "127.0.0.1"
        settings.tcpListenPort = "12444"
        settings.enableWebServer = True
        settings.webServerListenIp = "127.0.0.1"
        settings.webServerListenPort = "4567"

        self._dbSession.add(settings)
        self._dbSession.commit()

    def add_share(self, syncFolder, remoteHost, remotePath, remoteUser):
        share = self.Share(syncFolder, remoteHost, remotePath, remoteUser)
        self._dbSession.add(share)
        self._dbSession.commit()

    def remove_share(self, syncFolder):
        pass

    def get_shares(self):
        return self._dbSession.query(self.Share).all()

    shares = property(get_shares)

    def app_settings(self):
        return self._dbSession.query(self.Settings).first()

    def get_logLevel(self):
        return self.app_settings().logLevel

    def set_logLevel(self, logLevel):
        self.app_settings().logLevel = logLevel
        self._dbSession.commit()

    logLevel = property(get_logLevel, set_logLevel)

    def get_enableSystray(self):
        return self.app_settings().enableSystray

    def set_enableSystray(self, enable):
        self.app_settings().enableSystray = enable
        self._dbSession.commit()

    enableSystray = property(get_enableSystray, set_enableSystray)

    def get_tcpListenIp(self):
        return self.app_settings().tcpListenIp

    def set_tcpListenIp(self, ip):
        self.app_settings.tcpListenIp = ip
        self._dbSession.commit()

    tcpListenIp = property(get_tcpListenIp, set_tcpListenIp)

    def get_tcpListenPort(self):
        return self.app_settings().tcpListenPort

    def set_tcpListenPort(self, port):
        self.app_settings.tcpListenPort = port
        self._dbSession.commit()

    tcpListenPort = property(get_tcpListenPort, set_tcpListenPort)

    def get_enableWebserver(self):
        return self.app_settings().enableWebServer

    def set_enableWebserver(self, enable):
        self.app_settings.enableWebServer = enable
        self._dbSession.commit()

    enableWebServer = property(get_enableWebserver, set_enableWebserver)

    def get_webServerListenIp(self):
        return self.app_settings().webServerListenIp

    def set_webServerListenIp(self, ip):
        self.app_settings.webServerListenIp = ip
        self._dbSession.commit()

    webServerListenIp = property(get_webServerListenIp, set_webServerListenIp)

    def get_webServerListenPort(self):
        return self.app_settings().webServerListenPort

    def set_webServerListenPort(self, port):
        self.app_settings.webServerListenPort = port
        self._dbSession.commit()

    webServerListenPort = property(get_webServerListenPort, set_webServerListenPort)

    debugEnabled = False

    def add_test_share(self):
        """
        Adds some test shares
        """
        self.add_share("/Users/sruml/PythonDrop", "sebastianruml.com",
                "PythonDrop/PythonDrop.git", "pythondrop")

        self.add_share("/Users/sruml/PythonDrop2", "sebastianruml.com",
                "PythonDrop/PythonDrop.git", "pythondrop")

