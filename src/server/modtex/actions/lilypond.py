##
# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from __future__ import with_statement
from copy import copy
from xmlrpclib import Fault, Binary
from os.path import exists
from copy import copy

from modtex.action import Action
from modtex.types import Types
from modtex.constants import Constants
from modtex.facility import Facility
from modtex.execution import Execution, ExecutionError
from modtex.config import *

class Lilypond(Action):
    NAME = Types.LILYPOND
    TEMPLATE_FILE = Constants.TEMPLATE % \
                    {'file': NAME,
                     'suffix': Constants.MIMES[NAME].suffix}
    FACILITY = Config.facilities[NAME]

    def __init__(self, name=NAME, method=None, template_file=TEMPLATE_FILE,
                 facility=FACILITY):
        if method is None:
            method = self.render
        super(Lilypond, self).__init__(name, method, template_file, facility)

    def render(self, reddendum):
        OUTFILE = '-sOutputFile=%(outfile)s'
        IMAGE = '%(image)s.%(suffix)s'
        SOUND = '%(sound)s.%(suffix)s'
        IMAGE_MIME = Constants.MIMES[Types.PNG]
        SOURCE_MIME = Constants.MIMES[Types.LILYPOND]
        MEDIATOR_MIME = Constants.MIMES[Types.EPS]
        SOUND_MIME = Constants.MIMES[Types.MIDI]

        substituenda = {self.name: reddendum,
                        'version': self.facility.version}

        image = IMAGE % {'image': self.NAME, 'suffix': IMAGE_MIME.suffix}
        sound = SOUND % {'sound': self.NAME, 'suffix': SOUND_MIME.suffix}
        mediator = IMAGE % {'image': self.NAME, 'suffix': MEDIATOR_MIME.suffix}
        targets = {IMAGE_MIME.type: image,
                   SOUND_MIME.type: sound,
                   SOURCE_MIME.type: self.template_file}

        lilypond = self.facility
        ghostscript = Config.facilities[Types.GHOSTSCRIPT]
        executanda = [Execution(lilypond, args=[self.template_file]),
                      Execution(ghostscript,
                                args=[OUTFILE % {'outfile': image},
                                      mediator])]
        return super(Lilypond, self).render(substituenda, targets, executanda)
