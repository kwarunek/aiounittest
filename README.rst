aiounittest
===========

|image0|_ |image1|_

.. |image0| image:: https://api.travis-ci.org/kwarunek/aiounittest.png?branch=master
.. _image0: https://travis-ci.org/kwarunek/aiounittest

.. |image1| image:: https://badge.fury.io/py/aiounittest.svg
.. _image1: https://badge.fury.io/py/aiounittest

Info
====

This is a helper library to ease of your pain (and boilerplate), when writing a test of the asynchronous code (:code:`asyncio`). You can test:

* synchronous code (same as the :code:`unittest.TestCase`)
* asynchronous code, it supports syntax with :code:`async`/:code:`await` (Python 3.5+) and :code:`asyncio.coroutine`/:code:`yield from` (Python 3.4)

 
Installation
============

Use pip:

::

    pip install aiounittest

 
Usage
=====

It's as simple as use of :code:`unittest.TestCase`. Full docs at http://aiounittest.readthedocs.io.

.. code-block:: python

    import asyncio
    import aiounittest


    async def add(x, y):
        await asyncio.sleep(0.1)
        return x + y

    class MyTest(aiounittest.AsyncTestCase):

        async def test_async_add(self):
            ret = await add(5, 6)
            self.assertEqual(ret, 11)

        # or 3.4 way
        @asyncio.coroutine
        def test_sleep(self):
            ret = yield from add(5, 6)
            self.assertEqual(ret, 11)

        # some regular test code
        def test_something(self):
            self.assertTrue(true)

Library provide some additional tooling:

* async_test_,
* AsyncMockIterator_ to mock object for `async for`,
* futurized_ to mock coroutines.

.. _futurized: http://aiounittest.readthedocs.io/en/latest/futurized.html
.. _async_test: http://aiounittest.readthedocs.io/en/latest/async_test.html
.. _AsyncMockIterator: http://aiounittest.readthedocs.io/en/latest/asyncmockiterator.html

License
=======

MIT
