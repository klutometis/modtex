##
# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from os.path import abspath
from shutil import rmtree

class Cleanup(object):
    def __init__(self, directory):
        self.directory = directory

    def __del__(self):
        if not __debug__:
            rmtree(abspath(self.directory))
