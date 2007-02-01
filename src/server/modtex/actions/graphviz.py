##
# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from __future__ import with_statement
from xmlrpclib import Binary, Fault
from copy import copy

from modtex.execution import Execution, ExecutionError
from modtex.constants import Constants
from modtex.types import Types
from modtex.action import Action
from modtex.config import *

class Graphviz(Action):
    NAME = Types.GRAPHVIZ
    TEMPLATE_FILE = Constants.TEMPLATE % \
                    {'file': Types.GRAPHVIZ,
                     'suffix': Constants.MIMES[Types.GRAPHVIZ].suffix}
    FACILITY = Config.facilities[Types.GRAPHVIZ]

    def __init__(self, name=NAME, method=None, template_file=TEMPLATE_FILE,
                 facility=FACILITY):
        if facility.root is None:
            facility.root = Graphviz.FACILITY.root
        if facility.host is None:
            facility.host = Graphviz.FACILITY.host
        if facility.port is None:
            facility.port = Graphviz.FACILITY.port
        if facility.wait is None:
            facility.wait = Graphviz.FACILITY.wait
        if facility.path is None:
            facility.path = Graphviz.FACILITY.path
        if facility.args is None:
            facility.args = Graphviz.FACILITY.args
        if facility.verbose is None:
            facility.verbose = Graphviz.FACILITY.verbose
        if method is None:
            method = self.render
        super(Graphviz, self).__init__(name, method, template_file, facility)

    def render(self, reddendum):
        TARGET = '%(action)s.%(suffix)s'
        TARGET_MIME = Constants.MIMES[Types.PNG]
        SOURCE_MIME = Constants.MIMES[Types.GRAPHVIZ]

        substituenda = {Graphviz.NAME: reddendum}
        target = TARGET % {'action': Graphviz.NAME,
                           'suffix': TARGET_MIME.suffix}
        targets = {TARGET_MIME.type: target,
                   SOURCE_MIME.type: self.template_file}
        executandum = [Execution(self.facility, args=['-o', target,
                                                      self.template_file])]
        return super(Graphviz, self).render(substituenda, targets, executandum)
