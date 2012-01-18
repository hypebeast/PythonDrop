# Copyright (C) 2010-2012 Sebastian Ruml <sebastian.ruml@gmail.com>
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
from configobj import ConfigObj
#import xdg.BaseDirectory

from src import log


class ConfigError(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg


class Config:
    """
    Configuration system

    The configuration is stored in a text file. The configuration is structured
    in sections. Each section contains a set of options. Example:

        [section_name]
        some_list = ['some', 'list']
        some_string = 'foobar'
        some_int = 1
    """
    def __init__(self, config_file=None, default_config=None):
        """
        Load a config stored in the given file.

        @param config_file: the config filename to read
        @type config_file:  string or None. None implies to use
                            CONFIG_DIR/CONFIG_FILE
        """
        self._logger = log.Logger()

        self.first_load = False

        config_dir = None

        if config_file is not None:
            if not os.path.exists(config_file) or not open(config_file).read():
                config_file = self._create_config(config_file, default_config)

        self._filename = config_file

        try:
            self._config = ConfigObj(config_file, unrepr=True, list_values=True)
        except Exception, ex:
            errors = [ error.msg for error in ex.errors]
            errors = ';'.join(errors)
            #raise ConfigError("Config format error in %s: %s" % (config_file, errors))


    def get_filename(self):
        """ Config filename accessor

        @returns: the config filename from which the config has been read
        @rtype:   string
        """
        return self._filename


    def set_filename(self, filename):
        """
        Config filename setter

        Updates _config_dir and _filename private attributes

        @param filename: full path to the config file
        @type filename:  string
        """
        self._config.filename = filename
        self._filename = filename


    def _create_config(self, config_file, default_config):
        dirname = os.path.dirname(config_file)
        if dirname and not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except OSError, error:
                self.warning(error)
                raise ConfigError("Could not create %r : %r" % (dirname,
                                                                error))

        try:
            f = open(config_file,'w')
        except IOError, error:
            self.warning(error)
            raise ConfigError("Could not create %r : %s" % (config_file, error))

        f.write(default_config)
        f.close()
        self.first_load = True
        return config_file


    def get_option(self, key, section='general', default=None):
        """ Fetch the option value stored in the given section, at the
        given key. Return a default value if the key is not found.

        @param key:     the option key to look for
        @type key:      string
        @param section: the section name to search in
        @type section:  string
        @param default: the default value to use if the option is not found
        @type default:  object
        @returns:       value of given option in given section
        @rtype:         object
        """
        return self.get_section(section).get(key, default)


    def set_option(self, key, value, section='general'):
        """ Store an option value under key id at the given section.

        @param key:     the option key to look for
        @type key:      string
        @param value:   the value to store under given key
        @type value:    object
        @param section: the section name to search in
        @type section:  string
        """
        self._config.setdefault(section,{})[key] = value
        #self._config[section][key] = value


    def del_option(self, key, section='general'):
        """ Remove the option identified by key under the specified
        section.

        @param key:     the option key to look for
        @type key:      string
        @param section: the section name to search in
        @type section:  string
        """
        section_obj = self.get_section(section)
        if section_obj and key in section_obj:
            del section_obj[key]
        self.set_section(section, section_obj)


    def write(self, filename=None):
        """
        Save the config in a text file (handled by ConfigObj)

        """
        outfile = filename
        try:
            my_filename = self.get_filename()
            if not outfile:
                if my_filename:
                    outfile = open(my_filename, 'w')
            else:
                outfile = open(outfile, 'w')
        except IOError, error:
            pass
        else:
            if outfile:
                #self.info('Saving config to file %r' % outfile)
                self._config.write(outfile=outfile)


    def rename_section(self, old_name, new_name):
        """
        Rename a section of the config

        Options and comments stored in the section are kept intact.
        The config is update in-place. No result is returned by this
        method.

        @param old_name: the section to rename
        @type old_name:  string
        @param new_name: the new section name
        @type new_name:  string
        """
        section = self.get_section(old_name)
        if section:
            try:
                self._config.rename(old_name, new_name)
            except KeyError:
                pass


    def get_section(self, section_name, default=None):
        """
        Fetch a section from the config

        @param section_name: the section name to look for
        @type section_name:  string
        @param default:      the default value to use if the section is
                             not found
        @type default:       object
        @returns:            the ConfigObj section identified by section_name
        @rtype:              L{elisa.extern.configobj.ConfigObj} or empty dict
        """
        if default is None:
            default = {}
        return self._config.get(section_name, default)


    def set_section(self, section_name, section={}, doc={}):
        """
        Store section_data in a new section identified by section_name
        in the config

        @param section_name: the section name to update
        @type section_name:  string
        @param section:      the section data
        @type section:       dict
        @param doc:          documentation of section's options
        @type doc:           dict
        """
        if not isinstance(section, Section):
            section = Section(self._config,
                              self._config.depth+1,
                              self._config.main,
                              indict=section,
                              name=section_name)

            for key in section.keys():
                doc.setdefault(key, '')
            section.comments = dict([(k, ['# %s' % line
                                          for line in textwrap.wrap(v, 77)])
                                     for k,v in doc.iteritems()])
        if section.items():
            self._config[section_name] = section


    def del_section(self, section_name):
        """
        Remove the section identified by section_name

        @param section_name: the section name to delete
        @type section_name:  string
        """
        if self._config.has_key(section_name):
            del self._config[section_name]


    def as_dict(self):
        """
        Helper method to convert the Config instance to a dictionary

        @returns: a mapping of the config's options by section name
        @rtype: dict
        """
        r = {}
        for name, section in self._config.iteritems():
            r.update({name:section.dict()})
        return r


class clParser:
    """
    Command line management.
    """
    def __init__(self, parser):
        self.parser = parser
        self.addOptions()

    def parseArgs(self, HELP):
        return self.parser.parse_args()

    def addOptions(self):
        self.parser.add_option("-D", dest="debugmode",
                action="store_true", default=False,
                help="Starts PythonDrop in debug mode")
