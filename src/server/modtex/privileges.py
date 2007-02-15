# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
#
# @file
# Contains RootEscalationError and Privileges classes.
from syslog import syslog
from os import setregid, setgroups, setreuid, setuid, EX_NOPERM

class RootEscalationError(Exception):
    SAW = 'Process is yet able to become root'

    def __init__(self, saw=SAW):
        Exception.__init__(self, saw)

class Privileges(object):
    """ Composite of uid, gid """

    uid = gid = code = 0

    def __init__(self, uid, gid, code=0):
        self.uid = uid
        self.gid = gid
        self.code = code

    ##
    # Taking our queue from sendmail; and Chen, Wagner, Dean
    # (see <em>Setuid Demystified</em>, 2002): try to
    # escalate back to root, and fail if this nought
    # faileth.
    def drop(self):
        # Set group must be done before user.
        setregid(self.gid, self.gid)
        # Reduce supplementary groups
        setgroups([self.gid])
        # Finally, set user.
        setreuid(self.uid, self.uid)
        # Test that we cannot re-root
        try:
            setuid(0)
        except OSError:
            pass
        else:
            if code:
                print >> stderr, RootEscalationError().message
                exit(code)
            else:
                raise RootEscalationError()
