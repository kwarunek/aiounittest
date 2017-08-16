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

    def _runTestMethod(self, testMethod):
        loop = self.get_event_loop()
        ret = testMethod()
        try:
            future = asyncio.ensure_future(ret, loop=loop)
        except TypeError:
            # The test function is not awaitable.
            # Using `try/except` rather than iscoroutine due to support of 3.4 
            pass
        else:
            loop.run_until_complete(future)

    def run(self, result=None):
        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if (getattr(self.__class__, "__unittest_skip__", False) or
                getattr(testMethod, "__unittest_skip__", False)):
            # If the class or method was skipped.
            try:
                skip_why = (
                    getattr(self.__class__, '__unittest_skip_why__', '') or
                    getattr(testMethod, '__unittest_skip_why__', '')
                )
                self._addSkip(result, self, skip_why)
            finally:
                result.stopTest(self)
            return
        expecting_failure_method = getattr(testMethod,
                                           "__unittest_expecting_failure__", False)
        expecting_failure_class = getattr(self,
                                          "__unittest_expecting_failure__", False)
        expecting_failure = expecting_failure_class or expecting_failure_method
        outcome = _Outcome(result)
        try:
            self._outcome = outcome

            with outcome.testPartExecutor(self):
                self.setUp()

            if outcome.success:
                outcome.expecting_failure = expecting_failure
                with outcome.testPartExecutor(self, isTest=True):
                    self._runTestMethod(testMethod)
                outcome.expecting_failure = False

                with outcome.testPartExecutor(self):
                    self.tearDown()

            self.doCleanups()
            for test, reason in outcome.skipped:
                self._addSkip(result, test, reason)
            self._feedErrorsToResult(result, outcome.errors)
            if outcome.success:
                if expecting_failure:
                    if outcome.expectedFailure:
                        self._addExpectedFailure(result, outcome.expectedFailure)
                    else:
                        self._addUnexpectedSuccess(result)
                else:
                    result.addSuccess(self)
            return result
        finally:
            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()

            # explicitly break reference cycles:
            # outcome.errors -> frame -> outcome -> outcome.errors
            # outcome.expectedFailure -> frame -> outcome -> outcome.expectedFailure
            outcome.errors.clear()
            outcome.expectedFailure = None

            # clear the outcome, no more needed
            self._outcome = None
