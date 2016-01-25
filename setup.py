# coding=utf-8
# Copyright 2016 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from setuptools import setup, find_packages


setup(
  name = 'materiality.superstatic',
  packages = find_packages(),
  install_requires=[
    'Django>=1.7'
  ],
  test_suite='materiality.superstatic.management.commands._collectstatic_test',
  version = '0.1.1',
  description = 'Improved production deployment of static files in Django.',
  author = 'Benjy Weinberger',
  author_email = 'benjyw@gmail.com',
  license = 'MIT',
  url = 'https://github.com/materiality/superstatic',
  keywords = ['django', 'static', 'staticfiles', 'collectstatic'],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Framework :: Django :: 1.7',
    'Framework :: Django :: 1.8',
    'Framework :: Django :: 1.9',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
  ],
)
