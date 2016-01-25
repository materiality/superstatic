#!/usr/bin/env python2
#  coding=utf-8
# Copyright 2016 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import shlex
import subprocess


def _munge_cmd(cmd):
  if isinstance(cmd, (str, unicode)):
    args = shlex.split(cmd)
  else:
    args = cmd
  return args


def _execute(cmd):
  subprocess.check_call(_munge_cmd(cmd))


def verify_virtualenv():
  print('Checking virtualenv version.')
  try:
    _execute('virtualenv --version')
  except (OSError, subprocess.CalledProcessError):
    print('Installing virtualenv.')
    _execute('sudo pip install "virtualenv>=1.11,<1.12"')
  print('virtualenv installed.')


def verify_venv():
  verify_virtualenv()
  print('\nVerifying venv.')
  try:
    print('Checking venv python version.')
    _execute('./venv/bin/python2.7 --version')
  except OSError, subprocess.CalledProcessError:
    print('Creating venv.')
    _execute('virtualenv venv')
  print('Venv created.\n')


def verify_python_dependencies():
  print('\nVerifying python dependencies:')
  _execute('./venv/bin/pip install -r requirements.txt')
  print('Python dependencies installed.')


def setup():
  verify_venv()
  verify_python_dependencies()
  print('Done!')


if __name__ == '__main__':
  setup()

