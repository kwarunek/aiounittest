Usage
=====

To enable support for async tests just use :code:`aiounittest.AsyncTestCase` instead
of :code:`unittest.TestCase` (or decorate async test coroutines with :code:`async_test`). The :code:`futurized`
will help you to mock coroutines.

.. toctree::
   :maxdepth: 2

   asynctestcase
   async_test
   futurized
