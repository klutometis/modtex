.ig
mod_tex: distributed LaTeX-rendering over Apache
Copyright (C) 2007 Peter Danenberg
See doc/COPYING for details.
..
.so heading.ms
.so title.ms
.\" Footnotes-numbers trailed by `.'.
.nr FF 1
.\" Redefine footnote-numberer to have enclosing braces;
.\" but only in ascii.
.if '\*(.T'ascii' \{\
.       ds * [\\*[par@sup-start]\En+[fn*text-num]\\*[par@sup-end]]
.\}
