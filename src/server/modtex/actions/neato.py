# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from modtex.types import Types
from modtex.actions.graphviz import Graphviz
from modtex.facility import Facility
from modtex.config import *

class Neato(Graphviz):
    NAME = Types.NEATO
    TEMPLATE_FILE = Graphviz.TEMPLATE_FILE
    FACILITY = Config.facilities[Types.NEATO]

    def __init__(self, name=NAME, method=None, template_file=TEMPLATE_FILE, facility=FACILITY):
        if method is None:
            method = self.render
        super(Neato, self).__init__(name, method, template_file, facility)

    def render(self, reddendum):
        return super(Neato, self).render(reddendum)
