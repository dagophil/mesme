from .test_database import TestDatabase


def load_tests(loader, tests, pattern):
    """
    Load all tests from the imported modules into a test suite.
    :param loader: The test loader.
    :param tests: The standard tests that would be loaded by default.
    :param pattern: The pattern that is used in test discovery.
    :return: The test suite.
    """
    return tests
