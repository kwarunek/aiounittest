aiounittest
=======

|image0|_

.. |image0| image:: https://api.travis-ci.org/kwarunek/aiounittest.png?branch=master
.. _image0: https://travis-ci.org/kwarunek/aiounittest

Introduction
============

Library that let you to test the asynchornous code (`asyncio` only) transparently. This means you can test:
	- synchronous code (same as the `unittest.TestCase`)
	- asynchronous code, supports syntax with `async`/`await` (Python 3.5+) and `asyncio.coroutine`/`yield from` (Python 3.4)


Installation
============

You can use pip:

::

    pip install aiounitest

or manually

::

    git clone https://github.com/kwarunek/aiounittest.git
    cd aiounittest
    python setup.py install

Usage
=====

AsyncTestCase
----------

.. code-block:: python

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

futurized
----------

Helper that wraps given object in the asyncio's `Future`. It can be used to mock coroutines. Wrap any kind of object with it and pass to `unittest.mock.Mock`'s `return_value` or `side_effect`. If the object is an `Exception` (or a sublcass), futurized will treat that accordingly and exception will be raise upon await.

.. code-block:: python

    # dummy_math.py

    from asyncio import sleep

    async def add(x, y):
        await sleep(666)
        return x + y

.. code-block:: python

    from aiounittest import futurized, AsyncTestCase
    from unittest.mock import Mock, patch

    import dummy_math

    class MyTest(AsyncTestCase):

        async def test_add(self):
            mock_sleep = Mock(return_value=futurized('whatever'))
            patch('dummy_math.sleep', mock_sleep).start()
            ret = await dummy_math.add(5, 6)
            self.assertEqual(ret, 11)

        async def test_fail(self):
            mock_sleep = Mock(return_value=Exception('whatever'))
            patch('dummy_math.sleep', mock_sleep).start()
            with self.assertRaises(Exception) as e:
                await dummy_math.add(5, 6)


License
=======

MIT
