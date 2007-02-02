##
# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from modtex.types import Types
from modtex.constants import Constants
from modtex.action import Action
from modtex.execution import Execution
from modtex.facility import Facility
from modtex.config import *

class Gnuplot(Action):
    NAME = Types.GNUPLOT
    TEMPLATE_FILE = Constants.TEMPLATE % \
                    {'file': NAME,
                     'suffix': Constants.MIMES[NAME].suffix}
    FACILITY = Config.facilities[NAME]

    def __init__(self, name=NAME, method=None, template_file=TEMPLATE_FILE,
                 facility=FACILITY):
        if method is None:
            method = self.render
        super(Gnuplot, self).__init__(name, method, template_file, facility)

    def render(self, reddendum):
        TARGET = '%(action)s.%(suffix)s'
        TARGET_MIME = Constants.MIMES[Types.PNG]
        SOURCE_MIME = Constants.MIMES[Types.GNUPLOT]

        substituendum = {self.name: reddendum}
        target = TARGET % {'action': self.name,
                           'suffix': TARGET_MIME.suffix}
        targets = {TARGET_MIME.type: target,
                   SOURCE_MIME.type: self.template_file}
        gnuplot = self.facility
        executandum = [Execution(gnuplot, args=[self.template_file])]
        return super(Gnuplot, self).render(substituendum, targets, executandum)
