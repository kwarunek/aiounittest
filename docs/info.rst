What? Why? Next?
================

What?
-----

This module is a set of helpers to write simple and clean test for asyncio-based code.

Why?
----

Actually this is not nothing new, it just wraps current test approach in the handy utils.
There are couple libraries that try to solve this problem. This one:

- integrates nicely with standard :code:`unittest` library,
- is as simple as possible, without a bunch of stuff that is straithforward with unittest (eg re-inveting :code:`assertRaises` with `assertAsyncRaises`),
- supports both Python 3.5+ syntax and Python 3.4,
- it's well-documented (I think)

Among the others similar modules the best known is an extension pytest-asyncio_. It provides
couple extra features, but it cannot be used with `unittest.TestCase` (it does not support fixture injection).

Further reading:

- https://stackoverflow.com/questions/23033939/how-to-test-python-3-4-asyncio-code
- http://jacobbridges.github.io/post/unit-testing-with-asyncio/

.. _pytest: https://docs.pytest.org
.. _pytest-asyncio: https://pypi.python.org/pypi/pytest-asyncio

Next?
-----

- introduce :code:`AsyncMock`, ... Probably not, the :code:`unitest.mock.Mock` with :code:`futurized` is pretty simple.

- it would be great if `unittest` could support async test > `python-ideas`
