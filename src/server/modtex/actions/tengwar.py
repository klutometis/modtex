# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from modtex.actions.latex import Latex
from modtex.constants import Constants
from modtex.types import Types
from modtex.config import *

class Tengwar(Latex):
    NAME = Types.TENGWAR
    TEMPLATE_FILE = Constants.TEMPLATE % \
                    {'file': NAME,
                     'suffix': Constants.MIMES[Types.LATEX].suffix}
    FACILITY = Config.facilities[Types.LATEX]

    def __init__(self, name=NAME, method=None, template_file=TEMPLATE_FILE,
                 facility=FACILITY):
        if not method:
            method = self.render
        super(Tengwar, self).__init__(name, method, template_file, facility)

    def render(self, reddendum):
        return super(Tengwar, self).render(reddendum)
