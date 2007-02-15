# mod_tex: distributed LaTeX-rendering over Apache
# Copyright (C) 2007 Peter Danenberg
# See doc/COPYING for details.
from distutils.core import setup, Extension
from sys import path

path.insert(0, './src/server')

from modtex.config import *
from modtex.install import install_modtex
from modtex.install import install_root
from modtex.install import install_handler
from modtex.install import install_scripts
from modtex.install import install_docs
from modtex.build import build_modtex
from modtex.build import build_docs
from modtex.build import build_scripts

setup(name='modtex',
      version='0.1-beta',
      description='Distributed LaTeX-rendering over Apache',
      long_description=('Outsource heavy-weight and risky rendering to ' +
                        'segregated, unprivileged daemons.'),
      platforms='Linux',
      license='GPLv2',
      author='Peter Danenberg',
      author_email='<pcd at wikitex dot org>',
      url='http://modtex.org',
      package_dir={'modtex': 'src/server/modtex'},
      packages=['modtex', 'modtex.actions', 'modtex.config'],
      package_data={'modtex': ['templates/*']},
      data_files=[(Config.web, ['src/handler/.htaccess',
                               'src/handler/traderjoe.py'])],
      cmdclass={'build': build_modtex,
                'build_docs': build_docs,
                'build_scripts': build_scripts,
                'install': install_modtex,
                'install_root': install_root,
                'install_handler': install_handler,
                'install_scripts': install_scripts,
                'install_docs': install_docs,
                }
      )
