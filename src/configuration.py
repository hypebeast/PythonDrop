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
from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from sqlalchemy.orm import scoped_session, sessionmaker

import globals

Base = declarative_base()

class ConfigurationError(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg


class Configuration:
    def __init__(self):
        self._globals = globals.Globals()

        if not os.path.exists(self._globals.confDir):
            try:
                os.makedirs(self._globals.confDir)
            except OSError, error:
                pass

        if not os.path.exists(self._globals.cfgDb):
            # TODO: Create database
            # TODO: Create default config
            pass

        # Create the database
        self._engine = create_engine('sqlite:///' + self._globals.cfgDb, convert_unicode=True)
        #self._base = declarative_base()
        self._dbSession = scoped_session(sessionmaker(autocommit=False,
                                                    autoflush=False,
                                                    bind=self._engine))

        # Add some test data
        share = self.Share("/data", "git:/home/sruml/PythonDrop", "pythondrop")
        self._dbSession.add(share)
        #self._dbSession.commit()

    class Share(Base):
        __tablename__ = 'shares'

        id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
        polling_intervall = Column(Integer)
        path = Column(String(250))
        remote_name = Column(String(250))
        remote_user = Column(String(100))

        def __init__(self, path, remote_name, remote_user):
            self.path = path
            self.remote_name = remote_name
            self.remote_user = remote_user
            self.polling_intervall = 10


    class Settings(Base):
        __tablename__ = 'settings'

        id = Column(Integer, Sequence('user_id_seq'), primary_key=True)

        def __init__(self):
            pass
