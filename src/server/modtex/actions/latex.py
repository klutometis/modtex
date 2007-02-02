##
# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from __future__ import with_statement
from xmlrpclib import Binary, Fault
from glob import glob
from copy import copy

from modtex.cleanup import Cleanup
from modtex.constants import Constants
from modtex.types import Types
from modtex.action import Action
from modtex.config import *
from modtex.execution import Execution, ExecutionError

class Latex(Action):
    NAME = Types.LATEX
    TEMPLATE_FILE = Constants.TEMPLATE % \
                    {'file': NAME,
                     'suffix': Constants.MIMES[NAME].suffix}
    FACILITY = Config.facilities[NAME]

    def __init__(self, name=NAME, method=None, template_file=TEMPLATE_FILE,
                 facility=FACILITY):
        if method is None:
            method = self.render
        super(Latex, self).__init__(name, method, template_file, facility)

    ##
    # @param reddendum neuter singular gerund of reddere, &ldquo;to give back.&rdquo;
    # @param self reference
    # @return a dictionary comprising resultate image and source;
    # <tt>{'image/png': &ldquo;result&rdquo;, 'text/x-latex': &ldquo;source&rdquo;}</tt>.
    def render(self, reddendum):
        # Take only the first image produced by dvipng;
        # TODO: glob and deliver n images.  Could extend the
        # protocol to MIME: ARRAY(instances); see doc/TODO.
        TARGET = '%(action)s.%(suffix)s'
        TARGET_MIME = Constants.MIMES[Types.PNG]
        SOURCE_MIME = Constants.MIMES[Types.LATEX]

        substituendum = {self.name: reddendum}
        target = TARGET % {'action': self.name,
                           'suffix': TARGET_MIME.suffix}
        targets = {TARGET_MIME.type: target,
                   SOURCE_MIME.type: self.template_file}
        latex = self.facility
        dvipng = Config.facilities[Types.DVIPNG]
        executanda = [Execution(latex, args=[self.name]),
                      Execution(dvipng, args=['-o', target, self.name])]
        return super(Latex, self).render(substituendum, targets, executanda)
