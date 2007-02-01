.ig
mod_tex: distributed LaTeX-rendering over Apache
Copyright (C) 2007 Peter Danenberg
See doc/COPYING for details.
..
.so header.ms
.so title.ms
.TI README "README covers hortation and installation."
.XH 1 Prerequisites S 0
.XH 2 Server
.IP \(bu
Apache
.IP \(bu
mod_python
.IP \(bu
teTeX and dvipng (or TeX Live)
.IP \(bu
Python 2.5\**
.FS
We take advantage of with-statements which will become native in 2.6.
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
(Optional) Mount /usr/local/var/modtex on its own partition with NOSUID.
.IP \n+i.
Set up a chroot environment in /usr/local/var/modtex/latex for teTeX and dvipng.\**
.FS
See section 4, Chroot.
.FE
.IP \n+i.
Within the chroot, edit texmf.cnf to read:
.IP
.RS
shell_escape = f
.br
openout_any = p
.br
openin_any = p
.RE
.IP \n+i.
???
.IP \n+i.
Profit!
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
`modtex' and `modtex-debug' are installed by default in /usr/local/bin.  They both take `start' and `stop' as arguments, but `modtex-debug' provides some additional output to the syslog and keeps all work directories intact in /usr/local/var/modtex/latex/tmp for inspection.
.PP
`modtex-debug' also refrains from setting resource limits, since setting resource limits can introduce anti-intuitive errors and must be done with care.
.PP
`modtex', on the other hand, cleans up work directories (except in cases of resource-faults); and prints minimally to syslog.
.PP
`modtex' and `modtex-debug' need to be run as root to chroot into the rendering environment, but drop privileges immediately to modtex:modtex.
.XH 1 Configuration
.XH 2 Directories
.PP
mod_tex allows relatively fine-tuned control over the install-location, and provides some reasonable defaults.
.XH 2 Users
.PP
mod_tex also allows the ability to specify the nonprivileged user to whom it will drop after detaching from the console; it should be distinct from the Apache user, and ideally ad-hoc.
.XH 2 Facilities
.PP
Please inspect the facilities section to make sure that they correspond to your chroot environment; in particular, you will need to specify absolute paths to binaries.
.XH 2 Resources
.PP
mod_tex's resource managament has three layers: internal, kernel-enforced and per-user.
.XH 3 Internal
.PP
The `default_wait' dictionary provides fine-grained control over signals sent to runaway processes; `default_wait' works over and above RLIMIT_CPU, whose effects can be hard to predict.
.XH 3 Kernel-Enforced
.PP
Read more about kernel-limits in `man setrlimit'; mod_tex includes fairly Draconian policies which may need to be relaxed for production-sites.
.XH 3 Per-User
.PP
`ctime_unit' and `max_ctime_per_unit' provide ways to limit resource-usage from particular users.  mod_tex calculates how much CPU-time a user has usurped within one `ctime_unit'; if its usage exceeds `max_ctime_per_unit' with that unit of time, the request is temporarily denied.
.PP
The upshot is that users may have to submit several requests to complete a particularly time-consuming document.
.XH 1 Chroot
.PP
Chrooting is art and science; and can be risky if, for instance, you leave suid-binaries lying around.
.PP
Rebuild ld.so.cache within the jail after changing libs.
.PP
That said, Jailkit\**
.FS
http://olivier.sessink.nl/jailkit
.FE
and Makejail\**
.FS
http://www.floc.net/makejail
.FE
are useful utilities.
.XH 2 LaTeX
.PP
TeX Live\**
.FS
http://www.tug.org/texlive
.FE
provides a statically-linked dvipng in its full installation, and significantly reduces the library-overhead.
.PP
When running `install-tl.sh', supply the following (or similar) for TEXDIR:
.QP
\%/usr/local/var/modtex/latex/usr/local/texlive
.PP
The latex-facility in local.py may need to be adjusted accordingly; for instance:
.QP
\%/usr/local/texlive/bin/i386-linux/latex
.LP
in lieu of /usr/local/teTeX/bin/latex.
.XH 2 Graphviz
.PP
Using Jailkit, and after compiling GTK+, GLib, Pango, Cairo, Fontconfig and Graphviz with `--enable-static',\**
.FS
To make life easier, Graphviz was configured with `--disable-swig'; also, `/usr/local/bin/dot' must be manually linked to `dot_static'.
.FE
the following sufficed for our entry in `jk_init.ini':
.LP
.RS
.nf
[dot]
executables = /usr/local/bin/dot
directories = /lib, /usr/local/etc/pango, /usr/local/etc/fonts
directories = /usr/share/fonts, /usr/share/X11/fonts, /usr/local/lib/pango
regularfiles = /etc/ld.so.conf, /etc/ld.so.cache, /etc/passwd, /etc/group
regularfiles = /usr/local/bin/circo, /usr/local/bin/neato, /usr/local/bin/fdp
regularfiles = /usr/local/bin/twopi
.fi
.RE
.PP
In our experience, the cachedir for fontconfig should be changed\**
.FS
See /usr/local/etc/fonts/fonts.conf relative to the root.
.FE
from:
.QP
\%NONE/var/cache/fontconfig
.LP
to:
.QP
\%/var/cache/fontconfig
.LP
or else fontconfig will populate a local cache dir with each render, which is time consuming.
.PP
Next, either /var/cache/fontconfig should be rendered writable to modtex:modtex; or, preferably, graphviz run as root from within the jail to populate the cachedir.
.XH 1 Architecture
.PP
In short, an XML-RPC client (e.g., the MediaWiki-client) connects to the mod_python frontend (\(lqTrader Joe\(rq) served by Apache.
.PP
Trader Joe, in turn, connects to autonomous, unprivileged, chrooted d\(aemons sitting on arbitrary machines, that actually render the content.
.PP
After authentication,\**
.FS
Trader Joe uses basic-, but key-based-auth should be possible using curl's transport-layer.
.FE
but before Trader Joe befrays the rendering drones, he checks an IP->CPU-time database to see whether the client has used up their allotted rendering time.
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
