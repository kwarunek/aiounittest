import asyncio
import functools
import unittest
from unittest.case import _Outcome


class AsyncTestCase(unittest.TestCase):
    ''' AsyncTestCase allows to test asynchoronus function.

    This class can run:
        - test of synchronous code (same as the `unittest.TestCase`)
        - test of asynchronous code, supports syntax with `async`/`await` (Python 3.5+) and `asyncio.coroutine`/`yield from` (Python 3.4)

    Simple usage:

            import aiounittest

            class MyTest(aiounittest.AsyncTestCase):

                async def test_sleep(self):
                    await asyncio.sleep(1)
                    self.assertTrue(True)

    More examples in the `aiounittest`'s tests.

    To manage (eg change) event loop override the `get_event_loop` function.

    '''

    def get_event_loop(self, cleanup=True):
        loop = asyncio.get_event_loop()
        if cleanup:
            self.addCleanup(
                functools.partial(self._clean_up_event_loop, loop)
            )
        return loop

    def _clean_up_event_loop(self, loop):
        loop.close()
        self._recreate_event_loop()

    def _recreate_event_loop(self):
        ''' Creates brand new event loop

        AsyncTestCase explicitly close the default loop to manage cleanups.
        Here we create new one and make it default,
        so the asyncio is operational after the test.

        '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if name.startswith('test_'):  # and isinstance(attr, unction):
            return self._runTestMethod(attr)
        else:
            return attr

    def _runTestMethod(self, testMethod):
        @functools.wraps(testMethod)
        def wrapped(*args, **kwargs):
            loop = self.get_event_loop()
            ret = testMethod(*args, **kwargs)
            try:
                future = asyncio.ensure_future(ret, loop=loop)
            except TypeError:
                # The test function is not awaitable.
                # Using `try/except` rather than iscoroutine due to support of 3.4 
                pass
            else:
                loop.run_until_complete(future)
        return wrapped
