Testing
=======

All tests can be found in the
`tests directory <https://github.com/rheinwerk-verlag/planning-poker/tree/development/tests>`_. Before you can run the
tests, you should have a working :ref:`dev_docs/setup:Development Setup`.

Any changes to the existing code should still pass the test suite (there are of course exceptions where you'll have to
modify the tests in order for them to pass) and any new features should be covered by new tests.

Python Tests
------------

The Python tests are written using `pytest <https://docs.pytest.org/en/latest/>`_ and
`django-pytest <https://pytest-django.readthedocs.io/en/latest/>`_. In order to run them, use ::

$ pytest

JavaScript Tests
----------------

The JavaScript tests use the `Jest testing framework <https://jestjs.io>`_. Use ::

$ npm run test

to run the tests.
