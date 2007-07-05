# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from modtex.types import Types
from modtex.constants import Constants
from modtex.action import Action
from modtex.execution import Execution
from modtex.facility import Facility
from modtex.config import *

class SGF2DG(Action):
    NAME = Types.SGF2DG
    TEMPLATE_FILE = Constants.TEMPLATE % \
                    {'file': NAME,
                     'suffix': Constants.MIMES[NAME].suffix}
    FACILITY = Config.facilities[NAME]

    def __init__(self, name=NAME, method=None, template_file=TEMPLATE_FILE,
                 facility=FACILITY):
        if method is None:
            method = self.render
        super(SGF2DG, self).__init__(name, method, template_file, facility)

    def render(self, reddendum):
        SOURCE = '%(source)s.%(suffix)s'
        IMAGE = '%(image)s.%(suffix)s'
        SOURCE_MIME = Constants.MIMES[Types.SGF2DG]
        IMAGE_MIME = Constants.MIMES[Types.PNG]

        substituenda = {self.name: reddendum}
        source = SOURCE % {'source': self.NAME, 'suffix': SOURCE_MIME.suffix}
        image = IMAGE % {'image': self.NAME, 'suffix': IMAGE_MIME.suffix}
        targets = {IMAGE_MIME.type: image,
                   SOURCE_MIME.type: source}

        sgf2dg = self.facility
        tex = Config.facilities[Types.TEX]
        dvipng = Config.facilities[Types.DVIPNG]
        executanda = [Execution(sgf2dg, args=[self.name]),
                      Execution(tex, args=[self.name]),
                      Execution(dvipng, args=['-o', image, self.name])]
        return super(SGF2DG, self).render(substituenda, targets, executanda)
