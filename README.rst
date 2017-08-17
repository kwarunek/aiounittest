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

    pip install aiounitest

or manually

::

    git clone https://github.com/kwarunek/aiounittest.git
    cd aiounittest
    python setup.py install

Usage
=====

This library exposes following objects:

1. AsyncTestCase_
2. futurized_
3. async_test_

Each of them can be used independently.


AsyncTestCase
-------------

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


By default :code:`AsyncTestCase` use the main event loop and cleans it ups on every test. If you want to change that behaiour  override the :code:`AsyncTestCase.get_event_loop` method.

____________

futurized
----------

This helper wraps object in the asyncio's :code:`Future`. It can be used to mock coroutines. Decorate any kind of object with it and pass to :code:`unittest.mock.Mock`'s (:code:`MagicMock` as well) :code:`return_value` or :code:`side_effect`. If the given object is an :code:`Exception` (or its sublcass), :code:`futurized` will treat it accordingly and exception will be raised upon await.

Some dummy module:

.. code-block:: python

    # dummy_math.py

    from asyncio import sleep

    async def add(x, y):
        await sleep(666)
        return x + y


And the test with mocked :code:`asyncio.sleep`:

.. code-block:: python

    from aiounittest import futurized, AsyncTestCase
    from unittest.mock import Mock, patch

    import dummy_math

    class MyTest(AsyncTestCase):

        def tearDown(self):
            super().tearDown()
            patch.stopall()

        async def test_add(self):
            mock_sleep = Mock(return_value=futurized('whatever'))
            patch('dummy_math.sleep', mock_sleep).start()
            ret = await dummy_math.add(5, 6)
            self.assertEqual(ret, 11)

        async def test_fail(self):
            mock_sleep = Mock(return_value=futurized(Exception('whatever')))
            patch('dummy_math.sleep', mock_sleep).start()
            with self.assertRaises(Exception) as e:
                await dummy_math.add(5, 6)

____________

async_test
----------

It's a decorator that let you to use the standard `unittest.TestCase` and run asynchronous tests, just decorate them.

.. code-block:: python

    import asyncio
    import unittest
    from aiounittest import async_test


    async def add(x, y):
        await asyncio.sleep(0.1)
        return x + y

    class MyTest(unittest.TestCase):

        @async_test
        async def test_async_add(self):
            ret = await add(5, 6)
            self.assertEqual(ret, 11)


You can also pass the custom event loop with :code:`loop` argument. Note if the loop is provided, decorator won't close it.

.. code-block:: python

    import asyncio
    from aiounittest import async_test


    my_loop = asycio.get_event_loop()

    @async_test(loop=my_loop)
    async def my_func():
        await asyncio.sleep(1)
        return 'OK'

    # now call the function in the sync manner
    my_func()
    assert loop.is_closed() == False

Above examples also shows a handy way to call async code in sync way. If the name is a problem, the same functionality provide :code:`aiounittest.helpers.run_sync`. For example:

.. code-block:: python

    import asyncio
    from aiounittest.helpers import run_sync

    # using decorator syntax

    @run_sync
    async def my_func1():
        await asyncio.sleep(1)
        return 'OK1'

    ret = my_func1()
    print(ret)

    # using as a wrapper

    async def my_func2():
        await asyncio.sleep(1)
        return 'OK2'

    sync_my_func2 = run_sync(my_func2)
    ret = sync_my_func2()
    print(ret)

License
=======

MIT
