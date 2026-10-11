import asyncio
import unittest

from aiounittest import async_test


class RunSyncReuseTest(unittest.TestCase):
    def setUp(self):
        asyncio.set_event_loop(asyncio.new_event_loop())

    def tearDown(self):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            return
        loop.close()
        asyncio.set_event_loop(None)

    def test_default_loop_can_be_used_for_repeated_calls(self):
        loops = []

        @async_test
        async def wrapped(value):
            loops.append(asyncio.get_event_loop())
            return value

        self.assertEqual(wrapped(1), 1)
        self.assertTrue(loops[0].is_closed())
        self.assertEqual(wrapped(2), 2)
        self.assertTrue(loops[1].is_closed())
        self.assertIsNot(loops[0], loops[1])

    def test_default_loop_can_be_reused_after_an_exception(self):
        @async_test
        async def wrapped(value):
            if value < 0:
                raise ValueError('negative value')
            return value

        with self.assertRaisesRegex(ValueError, 'negative value'):
            wrapped(-1)
        self.assertEqual(wrapped(2), 2)

    def test_custom_loop_is_kept_for_repeated_calls(self):
        loop = asyncio.new_event_loop()
        self.addCleanup(loop.close)

        @async_test(loop=loop)
        async def wrapped():
            return asyncio.get_event_loop()

        self.assertIs(wrapped(), loop)
        self.assertIs(wrapped(), loop)
        self.assertFalse(loop.is_closed())
