# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
class Mime(object):
    ##
    # The mime-type (sometimes unprecedented).
    type = None

    ##
    # An (un)canonical file-suffix.
    suffix = None

    def __init__(self, type, suffix):
        self.type = type
        self.suffix = suffix
