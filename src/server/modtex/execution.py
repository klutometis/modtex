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
from subprocess import Popen, PIPE, STDOUT
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
        process = Popen(argumenta, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        timers = [Timer(time, self.kill, [process.pid, signal]) for time, signal in
                  self.facility.wait.iteritems()]
        for timer in timers:
            timer.start()
        if not self.stdin is None:
            with open(self.stdin) as stdin:
                (stdout, stderr) = process.communicate(stdin.read())
        else:
            (stdout, stderr) = process.communicate(None)
        if __debug__:
            for line in stdout.splitlines():
                syslog(line)
        status = process.returncode
        for timer in timers:
            # No penalty, btw, for cancelling a dead timer
            if timer.isAlive():
                timer.cancel()
        command = basename(self.facility.path)
        if (WEXITSTATUS(status) != EX_OK or WIFSIGNALED(status) or WIFSTOPPED(status)):
            raise ExecutionError(EX_SOFTWARE, stdout)
