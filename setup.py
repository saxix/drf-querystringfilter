#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import os
import re
import subprocess
import sys
import codecs
from distutils.errors import DistutilsError

from setuptools import setup, find_packages
from setuptools.command.sdist import sdist as BaseSDistCommand

ROOT = os.path.realpath(os.path.dirname(__file__))
init = os.path.join(ROOT, 'src', 'drf_querystringfilter', '__init__.py')
_version_re = re.compile(r'__version__\s+=\s+(.*)')
_name_re = re.compile(r'NAME\s+=\s+(.*)')

sys.path.insert(0, os.path.join(ROOT, 'src'))

with open(init, 'rb') as f:
    content = f.read().decode('utf-8')
    VERSION = str(ast.literal_eval(_version_re.search(content).group(1)))
    NAME = str(ast.literal_eval(_name_re.search(content).group(1)))


def read(*files):
    content = []
    for f in files:
        content.extend(codecs.open(os.path.join(ROOT, 'src', 'requirements', f), 'r').readlines())
    return "\n".join(filter(lambda l: not l.startswith('-'), content))


def check(cmd, filename):
    out = subprocess.run(cmd, stdout=subprocess.PIPE)
    f = os.path.join('src', 'requirements', filename)
    reqs = codecs.open(os.path.join(ROOT, f), 'r').readlines() or []
    existing = {re.split("(==|>=|<=>|<|)", name[:-1])[0] for name in reqs}
    declared = {re.split("(==|>=|<=>|<|)", name)[0] for name in out.stdout.decode('utf8').split("\n") if name and not name.startswith('-')}

    if existing != declared:
        msg = """Requirements file not updated.
Run 'make requiremets'
""".format(' '.join(cmd), f)
        raise DistutilsError(msg)

class SDistCommand(BaseSDistCommand):

    def run(self):
        checks = {'install.pip': ['pipenv', 'lock', '--requirements'],
                  'testing.pip': ['pipenv', 'lock', '-d', '--requirements']}

        for filename, cmd in checks.items():
            check (cmd, filename)
        super().run()


tests_requires = read('testing.pip')
install_requires = read('install.pip')

readme = codecs.open('README.rst').read()
history = codecs.open('CHANGES.rst').read().replace('.. :changelog:', '')

setup(name=NAME,
      version=VERSION,
      description="""Filter backend for DjangoRestFramework able to parse url parameters""",
      long_description=readme + '\n\n' + history,
      author='Stefano Apostolico',
      author_email='s.apostolico@gmail.com',
      url='https://github.com/saxix/drf-querystringfilter',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      install_requires=install_requires,
      tests_require=tests_requires,
      cmdclass={
          'sdist': SDistCommand,

      },
      extras_require={
          'dev': tests_requires,
          'test': tests_requires,
      },
      license="BSD",
      zip_safe=False,
      keywords='drf-querystringfilter',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
      ])
