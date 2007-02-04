##
# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from modtex.config import *

class Facility(object):
    root = host = port = path = wait = args = verbose = None

    def __eq__(self, other):
        return (self.root, self.host, other.port) == \
               (other.root, other.host, other.port)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, root=None, host=None, port=None, path=None,
                 wait=None, args=None, verbose=None, **kwargs):
        self.root = root
        self.host = host
        self.port = port
        self.path = path
        self.wait = wait
        self.args = args
        self.verbose = verbose
        for key, value in kwargs.iteritems():
            self.__setattr__(key, value)
