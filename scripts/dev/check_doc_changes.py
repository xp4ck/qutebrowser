#!/usr/bin/env python3
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2016-2020 Florian Bruhin (The Compiler) <mail@qutebrowser.org>

# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Check if docs changed and output an error if so."""

from __future__ import generator_stop, annotations

import sys
import subprocess
import os
import os.path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir,
                                os.pardir))

from scripts import utils

code = subprocess.run(['git', '--no-pager', 'diff', '--exit-code', '--stat',
                       '--', 'doc'], check=False).returncode

if os.environ.get('GITHUB_REF', 'refs/heads/master') != 'refs/heads/master':
    if code != 0:
        print("Docs changed but ignoring change as we're building a PR")
    sys.exit(0)

if code != 0:
    print()
    print('The autogenerated docs changed, please run this to update them:')
    print('   tox -e docs')
    print('   git commit -am "Update docs"')
    print()
    print('(Or you have uncommitted changes, in which case you can ignore '
          'this.)')
    if utils.ON_CI:
        utils.gha_error('The autogenerated docs changed')
        print()
        with utils.gha_group('Diff'):
            subprocess.run(['git', '--no-pager', 'diff'], check=True)
sys.exit(code)
