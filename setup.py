#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import distutils
import subprocess
from os.path import dirname, join

from setuptools import find_packages, setup
from setuptools.command.sdist import sdist
from wheel.bdist_wheel import bdist_wheel


def read(*args):
    return open(join(dirname(__file__), *args)).read()


class ToxTestCommand(distutils.cmd.Command):
    """Distutils command to run tests via tox with 'python setup.py test'.

    Please note that in our standard configuration tox uses the dependencies in
    `requirements/dev.txt`, the list of dependencies in `tests_require` in
    `setup.py` is ignored!

    See https://docs.python.org/3/distutils/apiref.html#creating-a-new-distutils-command
    for more documentation on custom distutils commands.
    """
    description = "Run tests via 'tox'."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.announce("Running tests with 'tox'...", level=distutils.log.INFO)
        return subprocess.call(['tox'])


def run_wrapper(self):
    """
    Wrapper around the `run` method of distutils or setuptools commands.

    The method creates the Javascript bundle file before the `run` method of the superclass is run.
    """
    self.announce("Creating the javascript bundle file...", level=distutils.log.INFO)
    return_code = subprocess.call(['npm', 'run', 'build'])
    if return_code is not 0:
        msg = "Error creating the javascript bundle file. Command exited with return code {}".format(return_code)
        self.announce(msg, level=distutils.log.ERROR)
        raise RuntimeError(msg)

    super(self.__class__, self).run()


def command_factory(name, base_class):
    """Factory method to create a distutils or setuptools command with a patched `run` method."""
    return type(str(name), (base_class, object), {'run': run_wrapper})


exec(read('planning_poker', 'version.py'))

classifiers = """\
# The next line is important: it prevents accidental upload to PyPI!
Private :: Do Not Upload
Development Status :: 2 - Pre-Alpha
Programming Language :: Python
<<<<<<< HEAD
Programming Language :: Python :: 3.6
Framework :: Django
Framework :: Django :: 3.0
=======
Programming Language :: Python :: 2.7
Framework :: Django
Framework :: Django :: 1.4
Framework :: Django :: 1.6
>>>>>>> master
Intended Audience :: Developers
License :: Other/Proprietary License
#Operating System :: Microsoft :: Windows
Operating System :: POSIX
#Operating System :: MacOS :: MacOS X
Topic :: Internet
"""

install_requires = [
    'channels>=2.4.0',
    'channels_redis>=2.4.2',
    'Django>=3.0.3',
    'django-auth-ldap>=2.1.1',
    'jira>=2.0.0',
    'psycopg2>=2.8.4'
]

tests_require = [
    'coverage',
    'flake8',
    'pydocstyle',
    'pylint',
    'pytest-django',
    'pytest-pep8',
    'pytest-cov',
    'pytest-pythonpath',
    'pytest',
]

setup(
    name='planning-poker',
    version=__version__,  # noqa
    description='A Django app which allows teams to perform a remote planning poker session',
    long_description=read('README.rst'),
    author='Rheinwerk Webteam',
    author_email='webteam@rheinwerk-verlag.de',
    maintainer='Rheinwerk Verlag GmbH Webteam',
    maintainer_email='webteam@rheinwerk-verlag.de',
    url='https://gitlab.intern.rheinwerk.de/rheinwerk/planning-poker',
    license='Proprietary',
    classifiers=[c.strip() for c in classifiers.splitlines()
                 if c.strip() and not c.startswith('#')],
    packages=find_packages(include=['planning_poker*']),
    include_package_data=True,
    test_suite='tests',
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={
        'test': ToxTestCommand,
        'sdist': command_factory('SDistCommand', sdist),
        'bdist_wheel': command_factory('BDistWheelCommand', bdist_wheel),
    }
)
