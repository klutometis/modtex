# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.

##
# @file
# @brief Command-line interface
#
# Contains the Execution and ExecutionError classes, which are responsible
# for interacting with the environment.
from __future__ import with_statement
from os import EX_SOFTWARE, kill, WIFEXITED, WIFSIGNALED, WIFSTOPPED, \
     WTERMSIG, WSTOPSIG, WEXITSTATUS, EX_OK
from syslog import syslog
from popen2 import Popen4
from threading import Timer, Thread
from os.path import basename
from signal import SIGKILL

from modtex.constants import Constants

##
# @brief Cacheable error
#
# To distinguish a command-line error (possibly syntax) from
# other internal errors.
class ExecutionError(Exception):
    def __init__(self, errno, strerr):
        Exception.__init__(self, errno, strerr)

##
# @brief Interaction with environment
#
# Execution does the actual dirty work of carrying out which
# commands.
class Execution(object):
    ##
    # Apposite execution environment
    facility = None

    ##
    # File to read and pass to process' stdin
    stdin = None

    ##
    # Extra args to append to facility's own
    args = []

    ##
    # @param facility execution-environment
    # @param self reference
    # @param args additional command-line arguments
    # @param stdin file to pipe to process' stdin
    def __init__(self, facility, args=[], stdin=None):
        self.facility = facility
        self.args = args
        self.stdin = None

    def kill(self, pid, signal):
        try:
            kill(pid, signal)
        except OSError:
            # Whoops: done-in, I believe, by a race condition
            # (e.g., the process finished while we were iterating
            # through timers).
            syslog('`%s\' met with a stale timer' % self.facility.path)
        
    ##
    # @callgraph
    def execute(self):
        argumenta = [self.facility.path]
        if not self.facility.args is None:
            argumenta.extend(self.facility.args)
        if __debug__ and not self.facility.verbose is None:
            argumenta.append(self.facility.verbose)
        argumenta.extend(self.args)
        process = Popen4(argumenta)
        timers = [Timer(time, self.kill, [process.pid, signal]) for time, signal in
                  self.facility.wait.iteritems()]
        for timer in timers:
            timer.start()
        Thread(target=lambda: process.fromchild.readlines()).start()
        status = process.wait()
        for timer in timers:
            # No penalty, btw, for cancelling a dead timer
            if timer.isAlive():
                timer.cancel()
        if not self.stdin is None:
            with open(self.stdin) as stdin:
                process.tochild.write(stdin.read())
        process.tochild.close()
        # Inefficient; by design? Should normally be run
        # !__debug__, anyway.
#         if __debug__:
#             while True:
#                 line = process.fromchild.readline()
#                 if line:
#                     syslog(line)
#                 else:
#                     break
        process.fromchild.close()
        command = basename(self.facility.path)
        if WIFEXITED(status):
            exit_status = WEXITSTATUS(status)
            if exit_status != EX_OK:
                raise ExecutionError(EX_SOFTWARE, '`%(command)s\' exited with \
                error-code %(exit_status)d' % {'command': command,
                                               'exit_status': exit_status})
        elif WIFSIGNALED(status):
            raise ExecutionError(EX_SOFTWARE, '`%(command)s\' terminated \
            with signal %(signal)d' % {'command': command,
                                       'signal': WTERMSIG(status)})
        elif WIFSTOPPED(status):
            raise ExecutionError(EX_SOFTWARE, '`%(command)s\' stopped with \
            signal %(signal)d' % {'command': command,
                                  'signal': WSTOPSIG(status)})
        else:
            # Failsafe: timers should have killed the process by this point, or
            # it should have ended naturally.
            kill(process.pid, SIGKILL)
            raise ExecutionError(EX_SOFTWARE, 'Failed timer on `%(command)s\'; \
            terminating the process extraordinarily.' % {'command': command})
