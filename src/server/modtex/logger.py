# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from syslog import syslog

class Logger(object):
    @staticmethod
    def write(scribendum):
        syslog(scribendum)
