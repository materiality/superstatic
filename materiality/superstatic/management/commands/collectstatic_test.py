# coding=utf-8
# Copyright 2016 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from contextlib import contextmanager
import os
import unittest
import shutil
import tempfile

import django
from django.conf import settings
from django.core.management import call_command
from django.test import TestCase as DjangoTestCase
from django.utils.six import StringIO

from materiality.superstatic.management.commands.collectstatic import Command



@contextmanager
def temporary_dir():
  """Yields an empty temporary directory, and cleans it up."""
  path = tempfile.mkdtemp()
  yield path
  shutil.rmtree(path)


class LoadPatternFileTest(unittest.TestCase):

  def test_load_patternfile(self):
    def do_test(expected, patterns):
      with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(patterns)
        tmp.flush()
        self.assertEqual(expected, Command.maybe_load_pattern_file(tmp.name))

    do_test([], '')
    do_test(['foo'], 'foo')
    do_test(['foo'], ' foo ')
    do_test(['foo'], ' foo ')
    do_test(['foo'], 'foo\n')
    do_test(['foo', 'bar'], 'foo\nbar\n')
    do_test(['foo', 'bar'], '# This is foo.\nfoo \n# This is bar.\n bar')
    do_test(['foo', 'bar', 'baz'], 'foo\nbar\n \nbaz\n\n')

  def test_nonexistent_patternfile(self):
    self.assertIsNone(Command.maybe_load_pattern_file('/nonexistent/file'))


class CollectStaticTest(DjangoTestCase):
  _dummy_db_dir = None

  @classmethod
  def setUpClass(cls):
    # Sadly, Django tests require at least a dummy database.
    cls._dummy_db_dir = tempfile.mkdtemp()
    # Note: the NAME setting must use forward slashes, even on Windows.
    dummy_db = os.path.join(cls._dummy_db_dir, 'dummy_db').replace(os.path.sep, '/')
    settings.configure(DATABASES={ 'default': { 'ENGINE': 'django.db.backends.sqlite3', 'NAME': dummy_db } },
                       INSTALLED_APPS=['materiality.superstatic'])
    django.setup()
    super(CollectStaticTest, cls).setUpClass()

  @classmethod
  def tearDownClass(cls):
    super(CollectStaticTest, cls).tearDownClass()
    if cls._dummy_db_dir:
      shutil.rmtree(cls._dummy_db_dir)

  def test_ignore_file(self):
    with temporary_dir() as tmpdir:
      # Create some static files.
      static_dir = os.path.join(tmpdir, 'static')
      os.mkdir(static_dir)

      def touch(relpath):
        with open(os.path.join(static_dir, relpath), 'w'):
          pass

      touch('file1.yes')
      touch('file2.no')
      touch('file3.yes')
      os.mkdir(os.path.join(static_dir, 'foo'))
      touch(os.path.join('foo', 'file4.no'))
      touch(os.path.join('foo', 'file5.yes'))
      touch(os.path.join('foo', 'file6.nono'))

      # Create the ignore file.
      ignore_file = os.path.join(tmpdir, 'static_ignores.txt')
      with open(ignore_file, 'w') as outfile:
        outfile.write(b'*.no\n*nono\n')

      expected_paths = ['file1.yes', 'file3.yes', os.path.join('foo', 'file5.yes')]

      # Run the command to collect the static files.
      static_root = os.path.join(tmpdir, 'collected_staticfiles')
      out = StringIO()
      with self.settings(STATIC_URL='/static/', STATIC_ROOT=static_root,
                         STATICFILES_DIRS=[static_dir],
                         SUPERSTATIC_IGNORE_FILE=ignore_file):
        call_command('collectstatic', stdout=out, interactive=False)

      # See which files were gathered.
      paths = []
      for dirpath, dirnames, filenames in os.walk(static_root):
        rel_dirpath = os.path.relpath(dirpath, static_root)
        for filename in filenames:
          paths.append(os.path.normpath(os.path.join(rel_dirpath, filename)))

      self.assertEquals(expected_paths, paths)
