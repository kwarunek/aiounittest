import asyncio
import functools
import unittest
from unittest.case import _Outcome
from .helpers import async_test


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

    def get_event_loop(self):
        return None

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if name.startswith('test_') and callable(attr):
            return async_test(attr, loop=self.get_event_loop())
        else:
            return attr
