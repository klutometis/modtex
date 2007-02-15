# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from pwd import getpwnam
from grp import getgrnam

try:
    from modtex.config.local import Config
except ImportError:
    from modtex.config.default import Config
    
Config.uid = getpwnam(Config.user).pw_uid
Config.gid = getgrnam(Config.group).gr_gid
Config.http_uid = getpwnam(Config.http_user).pw_uid
Config.http_gid = getgrnam(Config.http_group).gr_gid
