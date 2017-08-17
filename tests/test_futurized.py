from aiounittest import futurized, AsyncTestCase
from unittest.mock import Mock, patch

import dummy_math

class MyAddTest(AsyncTestCase):

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
