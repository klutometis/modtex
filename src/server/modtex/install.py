# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from __future__ import with_statement
from distutils.command.install import install
from distutils.core import Command
from distutils import log
from os import makedirs, umask, chown, chdir, mknod, makedev, chmod, \
     getcwd, stat, listdir, environ, system
from stat import S_IFCHR, S_IRUSR, S_IWUSR, S_IRGRP, S_IWGRP, S_IROTH, \
     S_IWOTH
from os.path import join, exists, realpath, dirname, isfile, basename
from shutil import copy
from glob import glob
from pwd import getpwnam
from grp import getgrnam
from subprocess import call

from modtex.config import *
from modtex.constants import Constants
from modtex.types import Types

def declare_copy(whence, whither):
    print '%(whence)s -> %(whither)s' % {'whence': whence,
                                         'whither': whither}
    copy(whence, whither)

def declare_chown(possidendum, uid, gid):
    print 'changing ownership of %(possidendum)s to %(uid)s:%(gid)s' % \
          {'possidendum': possidendum, 'uid': uid, 'gid': gid}
    chown(possidendum, uid, gid)

def declare_chmod(modificandum, modus):
    print 'modifying %(modificandum)s to %(modus)d' % \
          {'modificandum': modificandum, 'modus': modus}

class install_modtex(install):
    install.sub_commands.append(('install_root', lambda self:True))
    install.sub_commands.append(('install_handler', lambda self:True))
    install.sub_commands.append(('install_scripts', lambda self:True))
    install.sub_commands.append(('install_docs', lambda self:True))

class install_docs(Command):

    description = 'install documentation'

    user_options = [
        ('doc-dir=', 'd', 'whither docs'),
        ]

    def initialize_options(self):
        self.doc_dir = None

    def finalize_options(self):
        if self.doc_dir is None:
            self.doc_dir = Config.docs

    def run(self):
        UMASK = 0022
        DOCS = './doc'
        umask(UMASK)
        if not exists(self.doc_dir):
            makedirs(self.doc_dir)
        # Copy only a subset?
        for doc in listdir(DOCS):
            docfile = join(DOCS, doc)
            if isfile(docfile):
                declare_copy(docfile, self.doc_dir)

class install_scripts(Command):

    description = 'install entry points into mod_tex'

    user_options = [
        ('script-dir=', 's', 'where will lie scripts'),
        ]

    def initialize_options(self):
        self.script_dir = None

    def finalize_options(self):
        if self.script_dir is None:
            self.script_dir = Config.scripts

    def run(self):
        SCRIPT_DIR = './bin'
        SCRIPTS = ['modtex', 'modtex-debug']
        for scriptfilename in [join(SCRIPT_DIR, script) for script in SCRIPTS]:
            declare_copy(scriptfilename, self.script_dir)

class install_handler(Command):

    description = 'install Apache handler'

    user_options = [
        ('handler-dir=', 'h', 'where lieth target handler-dir'),
        ]

    def initialize_options(self):
        self.handler_dir = None

    def finalize_options(self):
        if self.handler_dir is None:
            self.handler_dir = Config.web

    def run(self):
        HANDLER = './src/handler'
        GLOBS = ['.htaccess', '*.py']

        if not exists(self.handler_dir):
            makedirs(self.handler_dir)
        declare_chown(self.handler_dir, Config.http_uid, Config.http_gid)
        for globs in GLOBS:
            for file in glob(join(HANDLER, globs)):
                # Will overwrite .htaccess modifications
                if isfile(file):
                    declare_copy(file, self.handler_dir)
                    declare_chown(join(self.handler_dir, basename(file)),
                                  Config.http_uid, Config.http_gid)
        if not exists(Config.db_root):
            makedirs(Config.db_root)
        declare_chown(Config.db_root, Config.http_uid, Config.http_gid)

class install_root(Command):
    description = 'create chroot skeleton'

    user_options = [
        ('root-dir=', 'd', 'directory whither common root'),
        ('temp-dir=', 't', 'temp directory within given root'),
    ]

    subradices = [
        Config.facilities[Types.LATEX].root,
        Config.facilities[Types.GRAPHVIZ].root,
        Config.facilities[Types.LILYPOND].root,
        Config.facilities[Types.GNUPLOT].root,
        ]

    def initialize_options(self):
        self.root_dir = None
        self.temp_dir = None

    def finalize_options(self):
        if self.root_dir is None:
            self.root_dir = Config.root
        if self.temp_dir is None:
            self.temp_dir = Constants.TEMP

    def run(self):
        UMASK = 0022
        DEV = Constants.DEV
        DEVICES = [(Constants.ZERO, 1, 5),
                   (Constants.NULL, 1, 3)]
        MODE = S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH
        DEVICE = 0
        MAJOR = 1
        MINOR = 2

        # 0644 by default
        umask(UMASK)
        # Create root
        if not exists(self.root_dir):
            makedirs(self.root_dir)
        # chdir(self.root_dir)
        
        for subradix in self.subradices:
            # Data dir in respective root (common to all modules)
            sub_root_temp_dir = join(self.root_dir, subradix, Constants.TEMP)
            if not exists(sub_root_temp_dir):
                makedirs(sub_root_temp_dir)
            declare_chown(sub_root_temp_dir, Config.uid, Config.gid)
            # Device directory
            dev = join(self.root_dir, subradix, DEV)
            if not exists(dev):
                makedirs(dev)
            # Create /dev/null and /dev/zero, setting appropriate
            # permissions
            for device in DEVICES:
                dev_device = join(dev, device[DEVICE])
                if not exists(dev_device):
                    mknod(dev_device, MODE | S_IFCHR,
                          makedev(device[MAJOR], device[MINOR]))
                    declare_chmod(dev_device, MODE)
