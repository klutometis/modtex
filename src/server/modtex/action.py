# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from __future__ import with_statement
from os.path import join, dirname
from xmlrpclib import Binary
from tempfile import mkdtemp
from os import rmdir, chdir
from hashlib import md5
from os.path import exists

from modtex.config import *
from modtex.constants import Constants
from modtex.cleanup import Cleanup

class Action(object):
    ## Where to find the action templates.
    LIBRARY_PATH = join(dirname(__file__), 'templates')

    ##
    # Construct.
    # @param self reference
    # @param name the action's name as referenced from the outside world,
    # i.e. XML-RPC handle.
    # @param method the internal method that responds to outward invocation
    # @param template_file whence to read the action's template
    # @param facility command-wrapper including root, args, path, etc. from
    # #modtex::config::default::Config
    def __init__(self, name, method, template_file, facility):
        super(Action, self).__init__(self, name, method, template_file, facility)
        self.name = name
        self.method = method
        self.template_file = template_file
        # Reads the template here, before chroot renders it
        # unavailable.
        with open(join(self.LIBRARY_PATH, template_file)) as template:
            self.template = template.read()
        self.facility = facility

    ##
    # Render the content. XXX: flag for whether or not
    # to return an incomplete subset of targets (with music,
    # for instance, that neglects to request midi).
    #
    # Populates the template file before calling executanda.
    # 
    # @param substituenda A dictionary of substitutions to make
    # in the template.
    # @param targets A dictionary of mime-types and apposite files.
    # @param self Reference.
    # @param executanda Commands to perform.
    def render(self, substituenda, targets, executanda):
        substitutum = self.template % substituenda
        cleanup = self.populate_tmpdir(substitutum)
        for executandum in executanda:
            executandum.execute()
        response = {}
        for mime, filename in targets.iteritems():
            if exists(filename):
                with open(filename) as file:
                    response[mime] = Binary(file.read())
        return response
                
    ##
    # Create and populate the work directory.
    # 
    # Create the temp directory; chdir thither; and register the
    # directory to be cleaned up, unless __debug__ is active (i.e.,
    # Python was started without -O).
    # 
    # @param substatutum The template with substitutions pre-rendered.
    # @param self Reference.
    # @return Reference to the cleanup mechanism that should
    # persist as long as needed.
    def populate_tmpdir(self, substatutum):
        temp_dir = mkdtemp(Constants.TEMP)
        chdir(temp_dir)
        with open(self.template_file, 'w') as template:
            template.write(substatutum)
        # Register deletion (unless __debug__) of temp_dir
        return Cleanup(temp_dir)
