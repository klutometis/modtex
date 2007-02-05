.ig
mod_tex: distributed LaTeX-rendering over Apache
Copyright (C) 2007 Peter Danenberg
See doc/COPYING for details.
..
.so header.ms
.so title.ms
.TI NEWS "\(lqNeotera\(rq were to the Athenians no good news; here, \
however, are our more visible mutations: violent, we hope, and benign."
.XH 1 News
.IP "Sun Feb  4 19:57:59 PST 2007"
We decided, again, to support XyMTeX as the default chemical interpreter.
.IP
I considered looking into a SMILES/InChi-to-graphics pathway;
but BKChem, the only interpreter that seems to do batch processing,
requires a framebuffer.
.IP
Also, an interesting discussion at WikiProject-Chemistry:\**
.FS
\%http://en.wikipedia.org/wiki/Wikipedia_talk:WikiProject_Chemistry/archive01
.FE
.IP
.RS
[SMILES is] okay for simple stuff, but for anything more complicated,
it becomes irritating to not be able to define the orientation that you
actually want in the diagram. For some things, it's impossible: try
getting any app to draw a metallocene legibly from SMILES :-)
.br
--Iridium77 23:09, 4 Mar 2004 (UTC)
.RE
.IP
The question is, therefore, XyMTeX vs. PPCHTeX:\**
.FS
\%http://en.wikipedia.org/wiki/User_talk:Sverdrup/Archive_2
.FE
.IP
.RS
The [downside] of [PPCHTeX] is that it handles anything other than plane
structures of five- and sixrings very badly.
.br
--Sverdrup 10:28, 20 Oct 2004 (UTC)
.RE
.IP
A compromise?  XyMTeX by default, possibly, and some flag or
non-standard tag to expose PPCHTeX.
.IP "Sun Feb  4 05:29:55 PST 2007"
Added support for FeynMF today (<feyn></feyn); recently gnuplot and
LilyPond made the cut.
.IP
During this phase we also spun-off mod_tex as a separate entity, and
WikiTeX as an ad-hoc Media\%Wiki client that connects thither.
.IP
Near term: finish off remaining classes (circuits?); may verzichten upon
Greek and Tipa, or give them unicode backends.
.so footer.ms
