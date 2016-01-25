# superstatic
Improved production deployment of static files in Django.

NOTE: This document assumes familiarity with Django's `django.contrib.staticfiles` app.

## Background 

The standard Django `collectstatic` command gathers all files it finds under all apps' `static` dirs, plus any
`STATICFILES_DIRS` specified in `settings.py`.  

However you may not want to deploy all the files you use during development.  For example, if you compile several
JavaScript source files into a single, minimized file for deployment, you probably don't want to deploy the
original source files, as they will be visible on the web to anyone who knows where to look.

The `collectstatic` command does have an `--ignore` flag, with which you can specify glob patterns of files that should
not be collected.  You can use this flag for finer-grained control over which files get deployed. However, you may
not have the option to modify the `collectstatic` invocation used during deployment. In particular, Heroku invokes
`collectstatic` for you, and that invocation's arguments cannot be configured.

## Solution

The `superstatic` app provides an enhanced `collectstatic` command, which can read ignore patterns from a file, 
and apply them without requiring any extra command-line arguments.

To use this in your Django project:

- Install superstatic, either with pip or by adding it to your `requirements.txt`.
- Add `materiality.superstatic` to your `INSTALLED_APPS`. Make sure to add it *before* `django.contrib.staticfiles`.
- Add `SUPERSTATIC_IGNORE_FILE = 'path/to/ignore_patterns_file'` to your `settings.py`.  That file should contain
  glob patters, one per line, as if passed to the `--ignore` flag. Blank lines and comment lines (beginning with `#`)
  are ignored.
