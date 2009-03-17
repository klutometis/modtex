.ig
mod_tex: distributed LaTeX-rendering over Apache
Copyright (C) 2007 Peter Danenberg
See doc/COPYING for details.
..
.so header.ms
.TI TODO "Things to do (exigenda) and things done (exacta) are recorded \
here."
.XH 1 Exigenda
.
.XH 2 Server
.IP Gnuplot
Parameters: size=\(lq{small,medium,large}\(rq
.IP
plot.gp and plot-cairo.gp, depending on backend
.IP Temp-dir
tmpwatch and cron
.IP Parse-trees
Bring back parse-trees, since Graphviz is not a drop-in replacement.
.IP Back-end
Transition to an array of chrooted Apaches; dump SimpleXMLRPCServer
on the back-end.
.IP Error-messages
Facilities-flag in default.py to return output from a process, giving
feedback; useful for: LaTeX or LilyPond, for instance, to disclose
syntax errors.
.IP
Not so useful for dvipng, etc. (sysadmins can retrieve that from the
syslog).
.IP
Some way to scrub sensitive data like paths? The chroot path-structure
is well documented, though.
.IP File-size
Limit requests to size X to avoid memory DoS?
.IP Graphviz
Optional link map (outsource source to external link)?
.IP Cache
Server-side cache (outsource?)
.IP Templates
Some protocol options to turn off templates for naked encoding (but not
for gnuplot, for instance, that depends upon the template to return
an image).
.IP Config
Windows-style config files (or XML?).
.IP Crontab
Crontab to delete daily cruft (left over from over-ambitious users who
outstrip resources, causing files.
.IP Actions
Plenary Classes
.IP Install
Replace ad-hoc installations by copytree; fail on directory existence.
.XH 3 "Multiple Documents"
.IP Protocol
Protocol change: return a dictionary of {MIME: ARRAY} objects; where
ARRAY is an array of matching documents (such as dvipng's image-per-
page).
.IP Structure
Breadth-first or depth-first: meaning, array of atomic dictionaries; or
an array of unbound arrays?
.IP
Second may be slightly more efficient in those cases where one source,
for instance, wields multiple targets (e.g., latex to multiple PNGs);
but more difficult to distinguish between uneven and incomplete data.
.IP
First may require some redundance (e.g., redundant MIDIs per LilyPond page,
or source per LaTeX image); but is cleaner, and determinant.
.IP
The superset renderer will have to receive a glob of targets; but how
does it distinguish between partitioned (e.g. PNGs) and whole (e.g. LaTeX-source)
data?
.IP
And if partitioned data should come back incomplete or in disparate quantities?
Can flag partitioned data, I suppose.
.IP
Bottom line: don't want to fuck up clean design; but may relent to multipage
output if necessary.  (LilyPond's eps driver, for instance, outputs the
whole document in one page; can link to an optional pdf if multi-page output
is desirable.)
.IP
General solution: offer optional alternative download (PDF, say) for
multipage docs, specified as parameter.
.
.XH 2 Documentation
.IP jailkit.ini
Document jk_init commands.
.IP Fontconfig
Fontconfig issue with NONE deposited in each directory.
.IP Doxygen
Real doxygen; what to do about docstrings, though? Answer: wait until
docutils matures into automatic reStructuredText extraction. (Doxygen
also does the nice call-graphs, though; and (who knows?) may do
docstrings at some point.)
.IP TODO
Raus; find something else: bugzilla?
.IP Permissions
Work with MediaWiki to restrict usage (optionally) to certain classes of
users.
.IP XML-RPC-lib
Add fallback-support for phpxmlrpc or Incutio for those with little
control over their installations, willing to take a performance hit.
.
.XH 2 Handler
.IP Throttle
A "check back in X seconds" message on over-usage.
.IP Database
Swap out home-brew lock system for some heavy-duty piece-of-shit (mysql,
say; postgre; or even sqlite3).
.
.XH 2 Jailkit
.IP Paths
Dynamic jailkit with gno-tools (./configure, etc.); throw in --with-user,
--with-group, etc.; or: make a build_jailkit target in setup.py.
.
.XH 1 Exacta
.IP "Server-client dichotomy"
Server is now its own entity: mod_tex; the client, a MediaWiki client,
is mod_tex.
.IP Packaging
Combine both server and client into a common package, or utterly segregated
(thus possibly not confusing the client-users)?
.IP
Latter: combined source; `src' directory: contains: `client', `server'.
.IP PHP-client
Basic request working; now to do something useful with it.
.IP Temp-dir
Does cleanup happen after exceptions? (The object is deleted, after all.)
.IP
Yes.
.IP "Python Apache-handler"
Trader Joe acts as a middle-man between locally running, unprivileged,
chrooted servers and the requesting public.
.IP
More efficient? Possibly; will rebuke the premature optimization for now.
.IP THANKS
Get Erik in there. Hephaistos, Hermes Charmophron, Apollon, Hestia, Hera,
Athena, dodeka Theoi.
.IP Footer/Header
mod_tex <VERSION> in footers or headers, across from date
.IP "Honest work in subserver"
Invocation of latex, dvipng
.IP "Web install"
Installs into web-root and changes ownership.
.IP "Title page"
ms-macro to institute title page (include with .so)
.IP License
Includable ms-file for license (.so)
.
.XH 2 Generic
.
.XH 3 Cache
.IP Purview
Client-, server-side or both?
.IP Failure
Problem: in 1.0+, failed rendering don't get cached and are rerendered
every day.
.IP
Distinguish, therefore, between server- and syntax-failures; and cache
accordingly.
.IP
No: a simple flag PHP side will turn on/off error caching; functioning
systems can turn it off for performance, and for debugging purposes:
back on.
.IP
It may be useful to distinguish between temporary and permanent errors,
now that we have ad-hoc classes.
.
.XH 2 Server
.IP Debug
Add a verbosity option on some facilities to be invoked when modtex-debug
is invoked; and quiet, otherwise.
.IP Config
Simplified on excision of client.
.IP "Resource Limits"
Don't setrlimits in case of debug.
.IP Facilities
Facility constructor takes merely a **kwargs, and populates accordingly;
no pre-set vars. (Implemented: pre-set args and **kwargs.)
.IP Debug
build_scripts command which takes --debug and disables optimization in
modtex-main.py
.IP
No: rather a modtex/main.py, and two trivial wrappers: modtex and modtex-
debug, which are invoked with `python -O' and `python' respectively.
.IP IP-throttle
Database of author vs. time
.IP setrlimit
Per-request (post droppriv)
.IP MIME-types
Currently a non-descript list in Constants; instantiate MIME-wrappers
with well-defined instance variables.
.IP Delivery
Client-server contract for the delivery of content (keys for XMLRPC
response); encode in a format parseable by PHP: XML, say?
.IP
Right now: using an implicit contract (image: content).  A low-tech
published API may suffice.
.
.XH 2 Client
.IP Source
`errors' directory to house the manifold.
.IP Authentication
CURL-lib on PHP can handle basic and key-based.
.IP Errors
Unified error presentation.
.IP Documentation
Own PHP-client documentation, or combined with server's (current).
.
.XH 3 Cache
.IP Purview
Use MediaWiki mechanism with its overhead, or some ad-hoc system?
.IP MediaWiki
MediaWiki mechanism: must be tweaked to forbid arbitrary upload; but can
detect orphaned files: Special:Unusedimages.
.IP
Must forge, apparently, a subclass of WebRequest, filling in artificial
values.
.IP Home-brew
Own mechanism: lightweight; but responsibility (cruft).
.
.XH 2 Documentation
.IP Territory
Copyright notices, etc.
.IP "README Mon Jan 22 08:36:11 PST 2007"
Installation
.IP "Build Sun Jan 21 01:46:55 PST 2007"
Build target in Setup.py which invokes the Makefile in doc.
.so footer.ms
