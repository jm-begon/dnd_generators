# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Authors: Jean-Michel Begon
#
# License: BSD 3 clause

from distutils.core import setup

NAME = 'dnd_generators'
VERSION = '0.0.dev'
AUTHOR = "Jean-Michel Begon"
AUTHOR_EMAIL = "jm.begon@gmail.com"
URL = 'https://github.com/jm-begon/dnd_generators/'
DESCRIPTION = 'A small utility to help generate stuff. The author does not claim ownership of the *data* used. Make sure you have a legal access to those before using this pacakge'
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()
CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.8',
    'Topic :: Utilities',
]

if __name__ == '__main__':
    setup(name=NAME,
          version=VERSION,
          author=AUTHOR,
          author_email=AUTHOR_EMAIL,
          url=URL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          license='BSD3',
          classifiers=CLASSIFIERS,
          platforms='any',
          install_requires=[],
          include_package_data=True,
          packages=['dnd_generators', "dnd_generators/fights",
                    "dnd_generators/npc", "dnd_generators/adventure"],
          )

