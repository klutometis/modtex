# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from __future__ import with_statement
from os import EX_USAGE, EX_NOPERM, kill, fork
from sys import argv, stderr
from glob import glob
from os.path import join
from signal import SIGTERM

from modtex.server import ModtexServer
from modtex.actions.math import Math
from modtex.actions.blockmath import BlockMath
from modtex.actions.chess import Chess
from modtex.actions.feyn import Feyn
from modtex.actions.dot import Dot
from modtex.actions.fdp import FDP
from modtex.actions.neato import Neato
from modtex.actions.circo import Circo
from modtex.actions.twopi import Twopi
from modtex.actions.lilypond import Lilypond
from modtex.actions.gnuplot import Gnuplot
from modtex.actions.xymtex import Xymtex
from modtex.actions.sgf2dg import SGF2DG
from modtex.actions.tengwar import Tengwar
from modtex.actions.greek import Greek
from modtex.config import *
from modtex.privileges import Privileges
from modtex.constants import Constants
from modtex.types import Types

USAGE = 'Usage: %(file)s start|stop' % {'file': __file__}

def err(error, code=0):
    print >> stderr, '%(file)s: %(error)s' % {'file': __file__,
                                              'error': error}
    if code:
        exit(code)
    
try:
    COMMAND, DIRECTIVE = argv
except ValueError:
    err(USAGE, EX_USAGE)

class Main(object):
    ACTIONS = {
        Types.LILYPOND: [Lilypond()],
        Types.GRAPHVIZ: [Dot(), FDP(), Neato(), Circo(), Twopi()],
        Types.LATEX: [Math(), Chess(), Feyn(), Xymtex(), Tengwar(),
                      Greek(), BlockMath()],
        Types.GNUPLOT: [Gnuplot()],
        Types.SGF2DG: [SGF2DG()],
        }

    def start(self):
        for actions in self.ACTIONS.values():
            # Must fork this bitch cuique actioni
            pid = fork()
            if pid:
                continue
            ModtexServer(actions)

    def stop(self):
        WILD_CARD = '*'
        ERR_NO_SUCH_PROCESS = 3

        # Drop to unprivileged user, kill the pids associated with
        # respective modtex servers. DRAWBACK: leaves pid-file-
        # skeletons behind; on the other hand, will not kill privileged
        # processes if pid files have been tampered with.
        #
        # A file-descriptor is left open in each process so as to maintain
        # a write-lock on the pid-file; worst case: it may be tampered with.

        # Drop privileges per configuration
        Privileges(Config.uid, Config.gid, EX_NOPERM).drop()
        for lockfilename in glob(join(Config.run, Constants.LOCKFILE % \
                                  {'application': Constants.APPLICATION % \
                                   {'action': WILD_CARD}})):
            with open(lockfilename) as lockfile:
                try:
                    pid_string = lockfile.read()
                    pid = int(pid_string)
                    kill(pid, SIGTERM)
                    err('Stopped `%(pid)d\'' % {'pid': pid})
                except ValueError:
                    if pid_string:
                        err('`%(lockfilename)s\' contains an invalid pid' % \
                            {'lockfilename': lockfilename})
                except OSError, (errno, strerror):
                    if errno != ERR_NO_SUCH_PROCESS:
                        err(('pid `%(pid)d\' from `%(lockfilename)s\' ' +
                             'cannot be killed: %(strerror)s') % \
                            {'pid': pid,
                             'strerror': strerror,
                             'lockfilename': lockfilename})

driver = Main()

try:
    {'start': driver.start, 'stop': driver.stop}[DIRECTIVE]()
except KeyError:
    err(USAGE, EX_USAGE)
