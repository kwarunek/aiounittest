AsyncTestCase
=============

Extends :code:`unittest.TestCase` to support asynchronous tests. Currently the most common solution is to explicitly run :code:`asyncio.run_until_complete` with test case. Aiounittest :code:`AsyncTestCase` wraps it, to keep the test as clean and simple as possible.

.. autoclass:: aiounittest.AsyncTestCase
   :members: get_event_loop
