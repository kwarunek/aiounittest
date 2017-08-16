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

or directly from Github

::

    pip install git+https://github.com/kwarunek/aiounittest.git

or manually

::

    git clone https://github.com/kwarunek/aiounittest.git
    cd aiounittest
    python setup.py install

Usage
=====

AsyncTestCase
----------

::

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


License
=======

MIT
