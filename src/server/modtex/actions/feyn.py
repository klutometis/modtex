# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
#
# @file
# Contains the Feynman class for doing Feynman diagrams
# over Thorsten Ohl's feynmf
# (http://www.ctan.org/tex-archive/macros/latex/contrib/feynmf/).
from modtex.action import Action
from modtex.actions.latex import Latex
from modtex.constants import Constants
from modtex.types import Types
from modtex.execution import Execution
from modtex.config import *

class Feyn(Latex):
    NAME = Types.FEYN
    TEMPLATE_FILE = Constants.TEMPLATE % \
                    {'file': NAME,
                     'suffix': Constants.MIMES[Types.LATEX].suffix}
    FACILITY = Config.facilities[Types.LATEX]

    def __init__(self, name=NAME, method=None, template_file=TEMPLATE_FILE,
                 facility=FACILITY):
        if not method:
            method = self.render
        super(Feyn, self).__init__(name, method, template_file, facility)

    def render(self, reddendum):
        IMAGE = '%(action)s.%(suffix)s'
        METAPOST = '%(action)s-mp.%(suffix)s'
        IMAGE_MIME = Constants.MIMES[Types.PNG]
        SOURCE_MIME = Constants.MIMES[Types.LATEX]
        METAPOST_MIME = Constants.MIMES[Types.METAPOST]

        substituendum = {self.name: reddendum}
        image = IMAGE % {'action': self.name,
                         'suffix': IMAGE_MIME.suffix}
        metapost_target = METAPOST % {'action': self.name,
                               'suffix': METAPOST_MIME.suffix}
        targets = {IMAGE_MIME.type: image,
                   SOURCE_MIME.type: self.template_file}
        latex = self.facility
        metapost = Config.facilities[Types.METAPOST]
        dvipng = Config.facilities[Types.DVIPNG]
        executanda = [Execution(latex, args=[self.name]),
                      Execution(metapost, args=[metapost_target]),
                      Execution(latex, args=[self.name]),
                      Execution(dvipng, args=['-o', image, self.name])]
        return Action.render(self, substituendum, targets, executanda)
