%% mod_tex: distributed LaTeX-rendering over Apache
%% Copyright (C) 2007 Peter Danenberg
%% See doc/COPYING for details.
\version "%(version)s"
\header {
  tagline = ""
}
\paper {
  printpagenumber = ##f
}
\score {
  {
%(music)s
  }
  \midi {}
  \layout {}
}
