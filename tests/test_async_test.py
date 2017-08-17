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
