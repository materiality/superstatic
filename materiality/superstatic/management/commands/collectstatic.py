# coding=utf-8
# Copyright 2016 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os

from django.conf import settings
from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectStaticCommand


class Command(CollectStaticCommand):
  help = 'Copies or symlinks static files into settings.STATIC_ROOT, reading ignore patterns from a file.'

  can_import_settings = True

  fixed_ignore_patterns = (
  )

  @classmethod
  def load_pattern_file(cls, path):
    with open(path, 'r') as infile:
      return [p for p in [p.strip() for p in infile] if p and not p.startswith('#')]

  @classmethod
  def maybe_load_pattern_file(cls, path):
    return cls.load_pattern_file(path) if os.path.isfile(path) else None

  def set_options(self, **options):
    super(Command, self).set_options(**options)
    ignore_file = getattr(settings, 'SUPERSTATIC_IGNORE_FILE', '')
    ignore_patterns_from_file = self.maybe_load_pattern_file(ignore_file)
    if ignore_patterns_from_file:
      self.ignore_patterns = list(set(self.ignore_patterns) | set(ignore_patterns_from_file))
