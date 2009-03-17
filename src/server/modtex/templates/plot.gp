##
# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
set term pngcairo size 800,600 font ",8" enhanced crop
set output 'plot.png'
%(plot)s
