Contributing to Planning Poker
==============================

First of all: Thanks for your interest in this project and taking the time to contribute.

Reporting bugs
---------------

If you have found a bug, please check the project's `issue <https://github.com/rheinwerk-verlag/planning-poker/issues>`_
page first and feel free to create a `new issue <https://github.com/rheinwerk-verlag/planning-poker/issues/new>`_, if no
one else has reported it yet.

When reporting a bug, it is helpful to include additional information about the problem you have encountered:
* A traceback and or screenshots of the issue
* The versions of the involved packages
* ideally a code example which can be used to consistently reproduce the bug

Making changes
--------------

Create a fork of this repository and follow the steps in the :ref:`dev_docs/setup:Development Setup` guide included in
order to get a running system. It is also advisable to at least skim through the
:ref:`dev_docs/index:Developer Documentation` to get an idea of the structure of this project.

Coding style
^^^^^^^^^^^^

We have created an `EditorConfig <https://editorconfig.org/>`_ file for this project that should be usable for most
IDEs. Otherwise please make sure to adhere to the specifications from the config file.

Python
""""""

The code follows the `PEP8 style guide <https://www.python.org/dev/peps/pep-0008/>`_ with the exception that the maximum
line length is 120 characters. You can use ``flake8`` with the configuration from the ``tox.ini`` file to check if your
changes conform with the rest of this project's code.

JavaScript and Vue
""""""""""""""""""

Follow `Google's style guide <https://google.github.io/styleguide/jsguide.html>`_ for the JavaScript code and
`Vue's style guide <https://vuejs.org/v2/style-guide/>`_ for the Vue specific code. The maximum line length also is 120
characters. There is currently no linting set up for these style guides.

Creating a pull request
^^^^^^^^^^^^^^^^^^^^^^^

Before creating a pull request make sure to check whether:

* Docstrings
   * Existing docstrings have to be updated
   * New code has valid and descriptive docstrings
* Tests
   * Existing `tests <https://github.com/rheinwerk-verlag/planning-poker/tree/development/tests>`_ have to be fixed
   * New code is covered by tests
   * All tests pass
* The documentation (in particular the
  `Sphinx documentation <https://github.com/rheinwerk-verlag/planning-poker/tree/development/docs>`_) has to be modified
* You updated the translations if you added or changed translated strings ::

    $ cd planning_poker
    $ python ../manage.py makemessages

  or mentioned in the pull request that there are missing translations

* Any user-facing changes are documented in the changelog
* You added yourself to the list of authors

