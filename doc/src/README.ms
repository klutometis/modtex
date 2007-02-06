.ig
mod_tex: distributed LaTeX-rendering over Apache
Copyright (C) 2007 Peter Danenberg
See doc/COPYING for details.
..
.so header.ms
.so title.ms
.TI README "README covers hortation and installation."
.XH 1 Prerequisites S 0
.IP \(bu
Apache
.IP \(bu
mod_python
.IP \(bu
Python 2.5
.IP \(bu
LaTeX, dvipng, etc.\**
.FS
See section 4, Chroot; the number of dependencies is proportional to the number of packages you'd like to support.
.FE
.XH 1 Installation
.PP
.XH 2 Server
.nr i 0 1
.IP \n+i.
Copy src/server/modtex/config/default.py to:
.IP
.RS
src/server/modtex/config/local.py
.RE
.IP \n+i.
Edit local.py to satisfaction.\**
.FS
See section 3, Configuration.
.FE
.IP \n+i.
Create user \(oqmodtex\(cq and \(oqmodtex\(cq-group.\**
.FS
Or whatever user and group was provided in \(oqlocal.py\(cq.
.FE
.IP \n+i.
Mount a file system on /usr/local/var/modtex with NOSUID (optional).
.IP \n+i.
Run:
.IP
.RS
python setup.py build
.RE
.IP
and:
.IP
.RS
sudo python setup.py install
.RE
.IP \n+i.
Set up as many chroot environments in /usr/local/var/modtex as you'd like to support.\**
.FS
See section 4, Chroot.
.FE
.XH 2 Handler
.PP
The Apache-handler mediates between the client and chrooted daemons; it requires mod_python.
.nr i 0 1
.IP \n+i.
Install mod_python,\**
.FS
http://www.modpython.org
.FE
if necessary.
.IP \n+i.
You may need to edit the .htaccess which was installed, by default, in:
.IP
.RS
\%/usr/local/apache2/htdocs/modtex/.htaccess
.RE
.XH 1 Execution
.PP
\(oqmodtex\(cq and \(oqmodtex-debug\(cq are installed by default in /usr/local/bin.
They both take \(oqstart\(cq and \(oqstop\(cq as arguments, but \(oqmodtex-debug\(cq provides
some additional output to the syslog and keeps all work directories intact
in /usr/local/var/modtex/<root>/tmp for inspection.
.PP
\(oqmodtex-debug\(cq also refrains from setting resource limits, since setting
resource limits can introduce anti-intuitive errors and must be done with
care.
.PP
\(oqmodtex\(cq, on the other hand, cleans up work directories (except in cases
of resource-faults); and prints minimally to syslog.
.PP
\(oqmodtex\(cq and \(oqmodtex-debug\(cq need to be run as root to chroot into the
rendering environment, but drop privileges immediately to modtex:modtex.
.XH 1 Configuration
.XH 2 Directories
.PP
mod_tex allows relatively fine-tuned control over the install-location,
and provides some reasonable defaults.
.XH 2 Users
.PP
mod_tex also allows the ability to specify the nonprivileged user to whom
it will drop after detaching from the console; it should be distinct from
the Apache user, and ideally ad-hoc.
.XH 2 Facilities
.PP
Please inspect the facilities section to make sure that they correspond to
your chroot environment; in particular, you will need to specify absolute
paths to binaries.
.XH 2 Resources
.PP
mod_tex's resource managament has three layers: internal, kernel-enforced
and per-user.
.XH 3 Internal
.PP
The \(oqdefault_wait\(cq dictionary provides fine-grained control over signals
sent to runaway processes; \(oqdefault_wait\(cq works over and above RLIMIT_CPU,
whose effects can be hard to predict.
.XH 3 Kernel-Enforced
.PP
Read more about kernel-limits in \(oqman setrlimit\(cq; mod_tex includes fairly
Draconian policies which may need to be relaxed for production-sites.
.XH 3 Per-User
.PP
\(oqctime_unit\(cq and \(oqmax_ctime_per_unit\(cq provide ways to limit resource-usage
from particular users.  mod_tex calculates how much CPU-time a user has
usurped within one \(oqctime_unit\(cq; if its usage exceeds \(oqmax_ctime_per_unit\(cq
with that unit of time, the request is temporarily denied.
.PP
The upshot is that users may have to submit several requests to complete a
particularly time-consuming document.
.XH 1 Chroot
.nr table 0
.PP
Chrooting is art and science; and can be risky if, for instance, you leave
suid-binaries lying around.
.PP
Modtex provides jailkit.ini in \(oqsrc/jailkit\(cq which, when used with
Olivier Sessink's Jailkit,\**
.FS
http://olivier.sessink.nl/jailkit
.FE
can help with the mechanics of chrooting.
.PP
Here's a mapping of actions to entities, for which see the relevant sections
below:
.nr table +1
.TS
center;
l s .
Table \*[SN]\n[table]. Actions and entities
_
.T&
l l .
Action	Entity
_
chemistry	LaTeX
chess	LaTeX
Feynman diagrams	LaTeX
go	sgf2dg
graphs	Graphviz
math	LaTeX
music	LilyPond
plotting	Gnuplot
_
.TE
.PP
Each jailed entity has prerequisite software, and relevant sections
of \(oqjailkit.ini\(cq.
.PP
Nota bene: ld.so.cache is not automatically copied to the root, and
needs to be rebuilt by running /sbin/ldconfig from within the root
after installation.
.PP
Nota item bene: \(oqjailkit.ini\(cq assumes that most packages were
build with \(oq--enable-static\(cq; YMMV.
.XH 2 LaTeX
.nr table 0
.IP Prerequisites:
LaTeX,\**
.FS
TeX Live (http://www.tug.org/texlive) has superseded teTeX (http://www.tug.org/tetex).
.FE
dvipng,\**
.FS
\%http://sourceforge.net/projects/dvipng
.FE
FreeType\**
.FS
For best results, enable the byte-code interpreter. http://www.freetype.org
.FE
.IP Jailkits:
latex, mktexpk, shell\**,
.FS
\(oqmktexpk\(cq, unfortunately, requires a shell; if you can build the
requisite PK files by manually chrooting into the environment, however,
you may be able to dispense with the shell.
.PP
Try generating the PKs by running a test-case through latex and dvipng.
.FE
dvipng, freetype
.IP "Additional packages:"
.nr table +1
.TS H
center;
l s s s .
Table \*[SN]\n[table]. Additional packages
_
.TH
.T&
l l l c .
Action	Package	Site	Included[a]
_
chem	XyMTeX	imt.chem.kit.ac.jp	
chess	skak	ctan.org	*
	skaknew	ctan.org	*
	texmate	ctan.org	*
feyn	FeynMF	ctan.org	*
math	AMS-LaTeX	ams.org	*
.T&
l s s s .
_
a. May be included in TeX Live.
.TE
.PP
Don't forget to manually run \(oqtexhash\(cq and \(oqupdmap\(cq from within
the chroot.
.XH 2 Gnuplot
.IP Prerequisites:
Gnuplot,\**
.FS
http://www.gnuplot.info
.FE
Fontconfig\**
.FS
http://www.fontconfig.org
.FE
.IP Jailkits:
gnuplot, fontconfig, fonts
.PP
IMPORTANT: disable system-calls in Gnuplot by applying the patch found in
\(oqsrc/patches\(cq before building Gnuplot; from Gnuplot's source directory,
issue:
.QP
.nf
patch -p1 < gnuplot-4.0.0-no-system.patch
.fi
.XH 2 LilyPond
.IP Prerequisites:
LilyPond,\**
.FS
http://lilypond.org
.FE
Guile,\**
.FS
http://www.gnu.org/software/guile/guile.html
.FE
Fontconfig,\**
.FS
http://www.fontconfig.org
.FE
Pango,\**
.FS
http://www.pango.org
.FE
Ghostscript\**
.FS
http://www.cs.wisc.edu/~ghost
.FE
.IP Jailkits:
guile, fontconfig, pango, ghostscript, fonts
.PP
For building LilyPond, there are more requisites; see \(oqINSTALL.txt\(cq.
.XH 2 Graphviz
.IP Prerequisites:
Graphviz,\**
.FS
http://www.graphviz.org
.FE
Pango,\**
.FS
http://www.pango.org
.FE
Fontconfig\**
.FS
http://www.fontconfig.org
.FE
.IP Jailkits:
pango, fontconfig, fonts
.PP
\(oqdot\(cq should be linked to \(oqdot_static\(cq before installation
(provided that you built with \(oq--enable-static\(cq).
.XH 2 sgf2dg
.IP Prerequisites:
sgf2dg,\**
.FS
http://match.stanford.edu/bump/go.html
.FE
LaTeX,\**
.FS
TeX Live (http://www.tug.org/texlive) has superseded teTeX (http://www.tug.org/tetex).
.FE
Perl\**
.FS
http://www.perl.com
.FE
.IP Jailkits:
latex, perl, dvipng, mktexpk
.PP
Since Perl is a significant requirement over and above basic LaTeX
packages, we decided to install sgf2dg in its own root for people
willing to incur the cost.
.XH 1 Architecture
.PP
In short, an XML-RPC client (e.g., the MediaWiki-client) connects to the
mod_python frontend (\(lqTrader Joe\(rq) served by Apache.
.PP
Trader Joe, in turn, connects to autonomous, unprivileged, chrooted d\(aemons
sitting on arbitrary machines, that actually render the content.
.PP
After authentication,\**
.FS
Trader Joe uses basic-, but key-based-auth should be possible using curl's
transport-layer.
.FE
but before Trader Joe befrays the rendering drones, he checks an IP->CPU-time
database to see whether the client has used up their allotted rendering time.
.ie '\*(.T'ps' \{\
.PS
C: ellipse "Client" "(PHP)";
spline right from C.r 1 "XML-RPC" "" "Authentication"<->;
T: ellipse "Trader Joe" "(Apache)";
spline right at T.r then up right then right <->;
ellipse width 1 "LaTeX" "d\(aemon" ;
spline right at T.r then right then right <->;
ellipse width 1 "LilyPond" "d\(aemon";
spline right at T.r then down right then right <->;
ellipse width 1 "Other" "d\(aemon";
.PE
.\}
.el \{\
.KS
.LD
                                         LaTeX-d\(aemon
                                        /
client<--(auth)-->traderjoe<--(resource)-->LilyPond-d\(aemon
                                        \\
                                         ...-d\(aemon
.DE
.KE
.\}
.PP
The d\(aemons should not be accessible to the intarweb at large.
.so footer.ms
