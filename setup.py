#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""setup.py for the versioning project"""

import os
from distutils.core import setup


# Declare __version_info__ and __version__ from the _version.py module code.
exec(open(os.path.join(os.path.dirname(__file__), 'src', 'versioning',
                       '_version.py')).read())


setup(
    name='versioning',
    version=__version__,
    author="Craig Hurd-Rindy",
    author_email="gnuworldman@gmail.com",
    maintainer="Craig Hurd-Rindy",
    maintainer_email="gnuworldman@gmail.com",
    url='https://github.com/',
    description="Version identifier management",
    long_description="""\
Manage version identifiers easily.
""",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        ],
    package_dir={'': 'src'},
    packages=['versioning'],
    )
