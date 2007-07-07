# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.

##
# @file
# @brief Configureth.
#
# Defines mutable parameters that should be tweaked for the local system
# (as opposed to #modtex::constants::Constants, which are relatively
# immutable).
#
# Copy to <tt>local.py</tt> before editing.
from signal import SIGTERM, SIGKILL
from resource import RLIMIT_CORE, RLIMIT_CPU, RLIMIT_FSIZE, RLIMIT_DATA, \
     RLIMIT_STACK, RLIMIT_RSS, RLIMIT_NPROC, RLIMIT_NOFILE, RLIMIT_OFILE, \
     RLIMIT_MEMLOCK, RLIMIT_AS
from os.path import join, dirname

from modtex.facility import Facility
from modtex.constants import Constants
from modtex.types import Types

##
# @brief Configuration.
# 
# Overridable configuration; should be copied to local.py before edition.
class Config(object):
    ## Where groupeth the sundry radices
    root = '/usr/local/var/modtex'
    ## Where rooteth the exposed web dir
    web = '/usr/local/apache2/htdocs/modtex'
    ## Dir to store executable scripts
    scripts = '/usr/local/bin'
    ## Dir to store documentation
    docs = '/usr/local/share/modtex'
    ## Dir that storeth process-identification
    run = '/var/run'
    ## Dir that containeth our play-dbs
    db_root = join(root, 'db')
    ## File that databaseth
    db = join(db_root, 'modtex')
    ## File that locketh writing
    db_lock = join(db_root, 'modtex.lock')
    ## User that runneth
    user = 'modtex'
    ## Group that o'er-runneth
    group = 'modtex'
    ## Apache-user
    http_user = 'nobody'
    ## Apache-group
    http_group = 'nobody'
    ## Haven where bindeth socket
    default_port = 8000
    ## Guest's correlative where bindeth socket
    default_host = '127.0.0.1'
    ## When and how to signal runaway children (independent of resource limits)
    default_wait = {45: SIGTERM,
                    50: SIGKILL}
    ## Specifica
    facilities = {
        Types.LATEX:
        Facility(root='latex',
                 host=default_host,
                 port=default_port + 0,
                 path='/usr/local/teTeX/bin/i686-pc-linux-gnu/latex',
                 wait=default_wait,
                 args=['-interaction=nonstopmode', '-no-shell-escape',
                       '-file-line-error', '-halt-on-error']),

        Types.DVIPNG:
        Facility(path='/usr/local/bin/dvipng',
                 wait=default_wait,
                 args=['--strict', '-l', '=1', '-bg', 'Transparent', '-T',
                       'tight'],
                 verbose='-v'),

        Types.METAPOST:
        Facility(path='/usr/local/teTeX/bin/i686-pc-linux-gnu/mpost',
                 args=['-file-line-error', '-halt-on-error',
                      '-interaction=nonstopmode'],
                 wait=default_wait),

        Types.GRAPHVIZ:
        Facility(root='graphviz',
                 host=default_host,
                 port=default_port + 1,
                 wait=default_wait,
                 args=['-Tpng:cairo'],
                 verbose='-v'),

        Types.DOT:
        Facility(path='/usr/local/bin/dot'),

        Types.FDP:
        Facility(path='/usr/local/bin/fdp'),

        Types.NEATO:
        Facility(path='/usr/local/bin/neato'),

        Types.CIRCO:
        Facility(path='/usr/local/bin/circo'),

        Types.TWOPI:
        Facility(path='/usr/local/bin/twopi'),

        Types.LILYPOND:
        Facility(root='lilypond',
                 host=default_host,
                 port=default_port + 2,
                 path='/usr/local/bin/lilypond',
                 wait=default_wait,
                 args=['-dsafe', '-dbackend=eps', '-f', 'ps'],
                 verbose='-V',
                 version='2.10'),

        Types.GHOSTSCRIPT:
        Facility(path='/usr/local/bin/gs',
                 wait=default_wait,
                 args=['-dEPSCrop', '-dGraphicsAlphaBits=4',
                       '-dTextAlphaBits=4', '-dNOPAUSE', '-dSAFER', '-dBATCH',
                       '-sDEVICE=png16m', '-r101']),

        Types.GNUPLOT:
        Facility(root='gnuplot',
                 host=default_host,
                 port=default_port + 3,
                 path='/usr/local/bin/gnuplot',
                 wait=default_wait),

        Types.SGF2DG:
        Facility(root='go',
                 host=default_host,
                 port=default_port + 4,
                 path='/usr/bin/sgf2dg',
                 wait=default_wait,
                 args=['-twoColumn'],
                 verbose='-verbose'),

        Types.TEX:
        Facility(path='/usr/local/teTeX/bin/i686-pc-linux-gnu/tex',
                 args=['-interaction=nonstopmode', '-no-shell-escape',
                       '-file-line-error', '-halt-on-error'],
                 wait=default_wait),
        }
    ## Selectively map public interfaces to private facilities;
    # values specify only host and port, and should therefore
    # be supersets (not strict) of the publicly exposed service.
    publicae = {
        Types.CHESS: facilities[Types.LATEX],
        Types.CIRCO: facilities[Types.GRAPHVIZ],
        Types.DOT: facilities[Types.GRAPHVIZ],
        Types.FDP: facilities[Types.GRAPHVIZ],
        Types.FEYN: facilities[Types.LATEX],
        Types.GNUPLOT: facilities[Types.GNUPLOT],
        Types.LILYPOND: facilities[Types.LILYPOND],
        Types.MATH: facilities[Types.LATEX],
        Types.NEATO: facilities[Types.GRAPHVIZ],
        Types.TWOPI: facilities[Types.GRAPHVIZ],
        Types.XYMTEX: facilities[Types.LATEX],
        Types.SGF2DG: facilities[Types.SGF2DG],
        Types.TENGWAR: facilities[Types.LATEX],
        }
    ## Process-ceiling for ForkingMixIn (independent of resource limits)
    max_children = 40
    ## Resource limits (see Constants for defaults).
    limits = {
        # Core file (don't produce them)
        RLIMIT_CORE: (0, 0),           
        # CPU time
        RLIMIT_CPU: (0, 0),
        # Maximum file size
        RLIMIT_FSIZE: (Constants.MiB, Constants.MiB),
        # (Un)initialized data plus heap
        RLIMIT_DATA: (0, 0),
        # Stack
        RLIMIT_STACK: (0, 0),
        # Resident set size (low memory conditions)
        RLIMIT_RSS: (0, 0),
        # Child processes                                        
        RLIMIT_NPROC: (2**3, 2**3),
        # Open files
        RLIMIT_NOFILE: (2**3, 2**3),
        # Memory lock
        RLIMIT_MEMLOCK: (0, 0),
        # Total available memory
        RLIMIT_AS: (2**6 * Constants.MiB, 2**6 * Constants.MiB),
        }
    ## Unit of processor time
    ctime_unit = 60.0
    ## Maximum processor time per unit processor time
    # that a client can usurp.
    max_ctime_per_unit = ctime_unit * 0.5
