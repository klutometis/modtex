##
# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from resource import RLIMIT_CORE, RLIMIT_CPU, RLIMIT_FSIZE, RLIMIT_DATA, \
     RLIMIT_STACK, RLIMIT_RSS, RLIMIT_NPROC, RLIMIT_NOFILE, RLIMIT_OFILE, \
     RLIMIT_MEMLOCK, RLIMIT_AS

from modtex.types import Types
from modtex.mime import Mime

class Constants(object):
    # Cacheable error-code
    EX_CACHEABLE = 2**15
    # That runneth
    APPLICATION = 'modtex-%(action)s'
    # Device-dir to relative root
    DEV = 'dev'
    # Null relative to dev
    NULL = 'null'
    # Zero relative to dev
    ZERO = 'zero'
    # Temp-dir to relative root
    TEMP = 'tmp'
    # Prograpso-glossia
    ENCODINGS = ['utf-8', 'ascii', 'latin-1']
    # Lock-file template
    LOCKFILE = '%(application)s.pid'
    # Mapping of internal type to mime-type, extension
    MIMES = {
        Types.EPS: Mime('application/postscript', 'eps'),
        Types.GNUPLOT: Mime('text/x-gnuplot', 'gp'),
        Types.GRAPHVIZ: Mime('text/x-graphviz', 'dot'),
        Types.LATEX: Mime('text/x-latex', 'tex'),
        Types.LILYPOND: Mime('text/x-lilypond', 'ly'),
        Types.METAPOST: Mime('text/x-metapost', 'mp'),
        Types.MIDI: Mime('audio/midi', 'midi'),
        Types.PNG: Mime('image/png', 'png'),
        }
    # Template-file-template
    TEMPLATE = '%(file)s.%(suffix)s'
    # Default resource limits
    LIMITS = {
        RLIMIT_CORE: (0L, -1L),
        RLIMIT_CPU: (-1L, -1L),
        RLIMIT_FSIZE: (-1L, -1L),
        RLIMIT_DATA: (-1L, -1L),
        RLIMIT_STACK: (8388608L, -1L),
        RLIMIT_RSS: (-1L, -1L),
        RLIMIT_NPROC: (16239L, 16239L),
        RLIMIT_NOFILE: (1024L, 1024L),
        RLIMIT_OFILE: (1024L, 1024L),
        RLIMIT_MEMLOCK: (32768L, 32768L),
        RLIMIT_AS: (-1L, -1L),
        }
    MiB = 2**20
    KiB = 2**10
